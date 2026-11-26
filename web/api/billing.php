<?php
// GitGame billing — DV-merchant (openpay.click). Config lives outside webroot (0600).
declare(strict_types=1);

require_once '/etc/gitgame/dv.php'; // returns ['key'=>..., 'client_key'=>..., 'merchant'=>...]

const DB_PATH = '/var/lib/gitgame/orders.sqlite';

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
    }
    return $pdo;
}

function prices(): array {
    static $p = null;
    if ($p === null) $p = json_decode(file_get_contents('/var/www/gitgame.live/api/prices.json'), true) ?: [];
    return $p;
}

/** Server-side price lookup: client only sends slug, never amount. */
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
