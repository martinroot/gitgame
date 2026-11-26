<?php
declare(strict_types=1);
require_once __DIR__ . '/billing.php';

$order_id = trim((string)($_GET['order_id'] ?? $_GET['order'] ?? ''));
if (!preg_match('/^gg-[a-f0-9]{12}$/', $order_id)) json_out(400, ['error' => 'bad order_id']);
$row = find_order($order_id);
$row ? json_out(200, order_payload($row)) : json_out(404, ['error' => 'not found']);
