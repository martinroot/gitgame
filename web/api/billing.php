<?php
// GitGame billing — DV-merchant (openpay.click). Config lives outside webroot (0600).
declare(strict_types=1);

require_once '/etc/gitgame/dv.php'; // returns ['key'=>..., 'client_key'=>..., 'merchant'=>...]

const DB_PATH = '/var/lib/gitgame/orders.sqlite';
const CATALOG = '/var/www/fapa.io/dsgame/catalog';

function db(): PDO {
    static $pdo = null;
    if ($pdo === null) {
        $pdo = new PDO('sqlite:' . DB_PATH, null, null, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        ]);
        $pdo->exec('create table if not exists orders(
            order_id text primary key,
            game_slug text not null,
            amount_usd real not null,
            wallet_id text,
            status text not null default "pending",
            created_at text default current_timestamp,
            paid_at text)');
        $cols = [];
        foreach ($pdo->query('pragma table_info(orders)') as $c) $cols[$c['name']] = true;
        if (!isset($cols['email'])) $pdo->exec('alter table orders add column email text');
        if (!isset($cols['receipt_sent'])) $pdo->exec('alter table orders add column receipt_sent integer default 0');
        $pdo->exec('create table if not exists order_items(
            order_id text not null,
            slug text not null,
            price real not null,
            primary key(order_id, slug))');
    }
    return $pdo;
}

function prices(): array {
    static $p = null;
    if ($p === null) $p = json_decode(file_get_contents('/var/www/gitgame.live/api/prices.json'), true) ?: [];
    return $p;
}

/** Server-side price lookup: client only sends slugs, never amounts. */
function price_for(string $slug): ?float {
    $p = prices();
    return isset($p[$slug]) ? (float)$p[$slug] : null;
}

function json_out(int $code, array $data): void {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

/** Create a DV-merchant deposit wallet for the order. Returns [wallet_id, pay_url]. */
function create_payment(string $order_id, float $amount_usd): array {
    $body = json_encode([
        'amount' => $amount_usd,
        'currency_code' => 'USD',
        'store_external_id' => $order_id,
    ]);
    $ch = curl_init(rtrim($GLOBALS['DV']['merchant'], '/') . '/api/v1/external/wallet');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $body,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 20,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json', 'X-Api-Key: ' . $GLOBALS['DV']['key']],
    ]);
    $raw = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    if ($code !== 200 || !$raw) {
        json_out(502, ['error' => 'payment service unavailable (' . $code . ')']);
    }
    $data = json_decode($raw, true)['data'] ?? null;
    if (!$data || empty($data['pay_url'])) {
        json_out(502, ['error' => 'payment service error']);
    }
    return [(string)$data['id'], (string)$data['pay_url']];
}

/** DV-NET webhook signature: HMAC-SHA256 over the raw request body with CLIENT_KEY. */
function check_signature(string $signature, string $raw_body): bool {
    $expected = hash_hmac('sha256', $raw_body, $GLOBALS['DV']['client_key']);
    return hash_equals($expected, strtolower(trim($signature)));
}

function mark_paid(string $order_id): bool {
    $st = db()->prepare("update orders set status='paid', paid_at=current_timestamp
        where order_id=? and status!='paid'");
    $st->execute([$order_id]);
    return $st->rowCount() > 0;
}

function body_json(): array {
    $raw = file_get_contents('php://input');
    $d = json_decode($raw, true);
    return is_array($d) ? $d : [];
}

/** Normalize and validate a cart: up to 20 unique slugs with server-side prices. */
function cart_slugs($input): array {
    $list = is_array($input) ? $input : [];
    if (!$list) return [];
    $list = array_values(array_unique(array_map('strval', $list)));
    if (count($list) > 20) json_out(400, ['error' => 'cart too large']);
    $out = [];
    foreach ($list as $slug) {
        if (!preg_match('/^[A-Za-z0-9_-]{1,100}$/', $slug)) json_out(400, ['error' => 'bad slug']);
        $price = price_for($slug);
        if ($price === null) json_out(404, ['error' => 'unknown game: ' . $slug]);
        $out[$slug] = $price;
    }
    return $out;
}

function valid_email($value): string {
    $email = strtolower(trim((string)$value));
    if (!filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($email) > 200) {
        json_out(400, ['error' => 'valid email required']);
    }
    return $email;
}

function find_order(string $order_id): ?array {
    $st = db()->prepare('select * from orders where order_id=?');
    $st->execute([$order_id]);
    $row = $st->fetch(PDO::FETCH_ASSOC);
    return $row ?: null;
}

function order_payload(array $row, bool $with_email = false): array {
    $st = db()->prepare('select slug, price from order_items where order_id=? order by slug');
    $st->execute([$row['order_id']]);
    $items = $st->fetchAll(PDO::FETCH_ASSOC);
    if (!$items && !empty($row['game_slug'])) {
        $items = [['slug' => $row['game_slug'], 'price' => (float)$row['amount_usd']]];
    }
    $out = [
        'order_id' => $row['order_id'],
        'amount_usd' => (float)$row['amount_usd'],
        'status' => $row['status'],
        'paid_at' => $row['paid_at'],
        'items' => $items,
    ];
    if ($row['status'] === 'paid') {
        $out['downloads'] = array_map(fn($i) => [
            'slug' => $i['slug'],
            'url' => '/api/download.php?order=' . urlencode($row['order_id']) . '&email=' . urlencode((string)($row['email'] ?? '')) . '&slug=' . urlencode($i['slug']),
        ], $items);
    }
    if ($with_email) $out['email'] = $row['email'];
    return $out;
}

/** Best-effort receipt: only when an MTA is installed; never blocks checkout. */
function send_receipt(string $email, array $order): void {
    if (!is_executable('/usr/sbin/sendmail')) return;
    $subject = 'GitGame order ' . $order['order_id'];
    $lines = ['Thank you for your purchase.', 'Order: ' . $order['order_id'],
              'Status: ' . $order['status'], 'Games:'];
    foreach ($order['items'] as $i) $lines[] = ' - ' . $i['slug'] . ' $' . number_format((float)$i['price'], 2);
    $lines[] = 'Your downloads: https://gitgame.live/account/?order=' . urlencode($order['order_id']) . '&email=' . urlencode($email);
    @mail($email, $subject, implode("\n", $lines), 'From: GitGame <noreply@gitgame.live>');
    db()->prepare('update orders set receipt_sent=1 where order_id=?')->execute([$order['order_id']]);
}
