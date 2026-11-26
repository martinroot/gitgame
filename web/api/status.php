<?php
declare(strict_types=1);
require_once __DIR__ . '/billing.php';

$order_id = trim((string)($_GET['order_id'] ?? ''));
if (!preg_match('/^gg-[a-f0-9]{12}$/', $order_id)) json_out(400, ['error' => 'bad order_id']);
$st = db()->prepare('select order_id, game_slug, amount_usd, status, paid_at from orders where order_id=?');
$st->execute([$order_id]);
$row = $st->fetch(PDO::FETCH_ASSOC);
$row ? json_out(200, $row) : json_out(404, ['error' => 'not found']);
