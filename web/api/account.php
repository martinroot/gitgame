<?php
declare(strict_types=1);
require_once __DIR__ . '/billing.php';

// Personal cabinet lookup: the client must know BOTH the order id and its email.
// Never list orders by email alone.
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $b = body_json();
    $order_id = trim((string)($b['order_id'] ?? $b['order'] ?? ''));
    $email = valid_email($b['email'] ?? '');
} else {
    $order_id = trim((string)($_GET['order_id'] ?? $_GET['order'] ?? ''));
    $email = valid_email($_GET['email'] ?? '');
}
if (!preg_match('/^gg-[a-f0-9]{12}$/', $order_id)) json_out(400, ['error' => 'bad order_id']);
$row = find_order($order_id);
if (!$row || strtolower((string)$row['email']) !== $email) json_out(404, ['error' => 'order not found']);
$out = order_payload($row, true);
if ($row['status'] === 'paid' && empty($row['receipt_sent'])) send_receipt($email, $out);
json_out(200, $out);
