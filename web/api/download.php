<?php
declare(strict_types=1);
require_once __DIR__ . '/billing.php';

// Paid downloads only. Requires order id + matching email + an item in that order.
$order_id = trim((string)($_GET['order'] ?? ''));
$email = valid_email($_GET['email'] ?? '');
$slug = trim((string)($_GET['slug'] ?? ''));
if (!preg_match('/^gg-[a-f0-9]{12}$/', $order_id) || !preg_match('/^[A-Za-z0-9_-]{1,100}$/', $slug)) {
    json_out(400, ['error' => 'bad request']);
}
$row = find_order($order_id);
if (!$row || $row['status'] !== 'paid' || strtolower((string)$row['email']) !== $email) {
    json_out(403, ['error' => 'order not paid or email mismatch']);
}
$st = db()->prepare('select 1 from order_items where order_id=? and slug=?');
$st->execute([$order_id, $slug]);
if (!$st->fetchColumn()) json_out(403, ['error' => 'game not in order']);

$root = realpath(CATALOG);
$dir = realpath(CATALOG . '/' . $slug);
if (!$root || !$dir || strpos($dir, $root . '/') !== 0 || !is_dir($dir)) json_out(404, ['error' => 'source not found']);

$zip = new ZipArchive();
$tmp = tempnam(sys_get_temp_dir(), 'ggzip');
if ($zip->open($tmp, ZipArchive::OVERWRITE) !== true) json_out(500, ['error' => 'zip error']);
$it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS));
$total = 0;
foreach ($it as $f) {
    $path = (string)$f;
    if ($f->isLink() || strpos($path, '/node_modules/') !== false || strpos($path, '/.git/') !== false) continue;
    $size = $f->getSize();
    if ($size > 20 * 1024 * 1024 || $total + $size > 150 * 1024 * 1024) continue;
    $zip->addFile($path, $slug . '/' . substr($path, strlen($dir) + 1));
    $total += $size;
}
$zip->close();
header('Content-Type: application/zip');
header('Content-Disposition: attachment; filename="' . $slug . '-source.zip"');
header('Content-Length: ' . filesize($tmp));
readfile($tmp);
unlink($tmp);
exit;
