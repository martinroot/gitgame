<?php
declare(strict_types=1);
require_once __DIR__ . '/billing.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') json_out(405, ['error' => 'POST only']);
$b = body_json();
$slug = trim((string)($b['slug'] ?? ''));
if ($slug === '' || strlen($slug) > 100) json_out(400, ['error' => 'slug required']);
$price = price_for($slug);
if ($price === null) json_out(404, ['error' => 'unknown game']);

$order_id = 'gg-' . bin2hex(random_bytes(6));
db()->prepare('insert into orders(order_id, game_slug, amount_usd) values(?,?,?)')
    ->execute([$order_id, $slug, $price]);
[$wallet_id, $pay_url] = create_payment($order_id, $price);
db()->prepare('update orders set wallet_id=? where order_id=?')->execute([$wallet_id, $order_id]);
json_out(200, ['order_id' => $order_id, 'pay_url' => $pay_url, 'amount' => $price]);
