<?php
declare(strict_types=1);
require_once __DIR__ . '/billing.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') json_out(405, ['error' => 'POST only']);
$b = body_json();
$raw_slugs = $b['slugs'] ?? (isset($b['slug']) ? [$b['slug']] : []);
$cart = cart_slugs($raw_slugs);
if (!$cart) json_out(400, ['error' => 'cart is empty']);
$email = valid_email($b['email'] ?? '');
$amount = round(array_sum($cart), 2);
$slugs = array_keys($cart);

$order_id = 'gg-' . bin2hex(random_bytes(6));
$db = db();
$db->beginTransaction();
try {
    $db->prepare('insert into orders(order_id, game_slug, amount_usd, email) values(?,?,?,?)')
       ->execute([$order_id, $slugs[0], $amount, $email]);
    $st = $db->prepare('insert into order_items(order_id, slug, price) values(?,?,?)');
    foreach ($cart as $slug => $price) $st->execute([$order_id, $slug, $price]);
    $db->commit();
} catch (Throwable $e) {
    $db->rollBack();
    json_out(500, ['error' => 'could not create order']);
}

[$wallet_id, $pay_url] = create_payment($order_id, $amount);
db()->prepare('update orders set wallet_id=? where order_id=?')->execute([$wallet_id, $order_id]);
json_out(200, [
    'order_id' => $order_id,
    'pay_url' => $pay_url,
    'amount' => $amount,
    'email' => $email,
    'items' => array_keys($cart),
]);
