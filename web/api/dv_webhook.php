<?php
declare(strict_types=1);
require_once __DIR__ . '/billing.php';

$raw = file_get_contents('php://input');
$sig = $_SERVER['HTTP_X_SIGNATURE'] ?? '';
if (!check_signature($sig, $raw)) {
    http_response_code(403);
    exit;
}
$p = json_decode($raw, true);
$order_id = (string)($p['store_external_id'] ?? '');
$type = (string)($p['type'] ?? '');
if ($type === 'PaymentReceived' && $order_id !== '' && strpos($order_id, 'gg-') === 0) {
    mark_paid($order_id); // idempotent: only flips pending -> paid
    $row = find_order($order_id);
    if ($row && !empty($row['email']) && empty($row['receipt_sent'])) {
        send_receipt($row['email'], order_payload($row, true));
    }
}
http_response_code(200);
echo 'OK';
