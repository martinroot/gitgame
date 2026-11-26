#!/usr/bin/env python3
"""
catalog_purge.py — снос битых/неразмеченных игр из каталога fapa.io/dsgame/catalog.

Работает через root-ssh на 127.0.0.1 (как auto_deploy.py / junk_purge.py):
владелец каталога — www-data, пользователь drogame прав не имеет.

Удаляет:
  * карточки из catalog.json по списку слагов (атомарно, под flock);
  * папку игры;
  * превью thumbs/<slug>.jpg.

Перед правкой catalog.json делает бэкап catalog.json.bak-<ts>.

  python3 catalog_purge.py --dry --slugs a,b --unmarked
  python3 catalog_purge.py --slugs a,b --unmarked
"""
import argparse
import base64
import json
import os
import re
import subprocess

FAPA_PASS = os.environ.get('FAPA_PASS', '')
FAPA_CAT = '/var/www/fapa.io/dsgame/catalog'
SLUG_RE = re.compile(r'^[A-Za-z0-9._-]+$')


def ssh(cmd, t=180):
    return subprocess.run(
        ['sshpass', '-e', 'ssh', '-o', 'StrictHostKeyChecking=no', 'root@127.0.0.1', cmd],
        capture_output=True, text=True, timeout=t, env={**os.environ, 'SSHPASS': FAPA_PASS})


# Атомарная правка catalog.json под flock + удаление папок/превью — одним PHP.
PHP = r'''<?php
$dir = "%s";
$rm = json_decode(base64_decode("%s"), true);
if (!is_array($rm)) $rm = [];
$f = "$dir/catalog.json";
$bak = $f . ".bak." . time();
copy($f, $bak);
$fh = fopen($f, "c+");
if (!$fh) { echo "err-io"; exit; }
flock($fh, LOCK_EX);
$c = json_decode(stream_get_contents($fh), true);
if (!is_array($c)) $c = [];
$set = array_flip($rm);
$before = count($c);
$c = array_values(array_filter($c, fn($g) => !isset($set[$g["slug"] ?? ""])));
ftruncate($fh, 0); rewind($fh);
fwrite($fh, json_encode($c, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
flock($fh, LOCK_UN); fclose($fh);
function rr($p) {
  if (is_link($p) || is_file($p)) { @unlink($p); return; }
  if (!is_dir($p)) return;
  foreach (scandir($p) as $e) { if ($e === "." || $e === "..") continue; rr("$p/$e"); }
  @rmdir($p);
}
$base = realpath($dir);
$removed = 0;
foreach ($rm as $s) {
  if (!preg_match("/^[A-Za-z0-9._-]+$/", $s)) continue;
  $gd = realpath("$dir/$s");
  if ($gd && strpos($gd, $base . DIRECTORY_SEPARATOR) === 0) { rr($gd); $removed++; }
  @unlink("$dir/thumbs/$s.jpg");
}
echo "catalog: $before -> " . count($c) . "; dirs_removed: $removed; backup: $bak";
'''


def php_purge(slugs):
    body = PHP % (FAPA_CAT, base64.b64encode(json.dumps(slugs).encode()).decode())
    out = ssh('php -r ' + subprocess.list2cmdline([body]), t=120)
    return (out.stdout or '').strip() + ((' ERR:' + out.stderr.strip()) if out.stderr else '')


def catalog():
    out = ssh('cat %s/catalog.json' % FAPA_CAT).stdout
    try:
        return json.loads(out)
    except Exception:
        return []


def unmarked_dirs():
    """Папки игр без карточки в catalog.json (бэкапы/файлы — не папки игр)."""
    slugs = {g.get('slug', '') for g in catalog()}
    out = ssh('find %s -mindepth 1 -maxdepth 1 -type d -printf "%%f\\n"' % FAPA_CAT).stdout.split()
    return [n for n in out if n and n != 'thumbs' and n not in slugs]


def dir_state(slug):
    """Что реально лежит в папке на сервере."""
    out = ssh('ls -1 %s/%s 2>/dev/null | head -3' % (FAPA_CAT, slug)).stdout.strip()
    n = ssh('find %s/%s -type f 2>/dev/null | wc -l' % (FAPA_CAT, slug)).stdout.strip()
    sz = ssh('du -sm %s/%s 2>/dev/null | cut -f1' % (FAPA_CAT, slug)).stdout.strip()
    return out.split('\n')[:3], n, sz


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--slugs', default='')
    ap.add_argument('--slugs-file', default='')
    ap.add_argument('--unmarked', action='store_true',
                    help='добавить папки без карточки в catalog.json')
    ap.add_argument('--no-folder', action='store_true',
                    help='не удалять папки игр (только карточки и превью)')
    args = ap.parse_args()

    slugs = []
    if args.slugs:
        slugs += [s.strip() for s in args.slugs.split(',') if s.strip()]
    if args.slugs_file:
        with open(args.slugs_file, encoding='utf-8') as fh:
            slugs += [ln.strip() for ln in fh if ln.strip()]
    if args.unmarked:
        slugs += unmarked_dirs()
    slugs = sorted({s for s in slugs if SLUG_RE.match(s)})

    if not slugs:
        print('нечего удалять')
        return

    print('кандидатов на снос: %d' % len(slugs))
    for s in slugs:
        top, n, sz = dir_state(s)
        print('   %-38s files=%-5s size=%sM  %s' % (s, n or '0', sz or '0', ', '.join(top[:2])))

    if args.dry:
        print('\nDRY-режим: ничего не удалено')
        return

    print('\n' + php_purge(slugs))
    left = len(catalog())
    print('в каталоге осталось карточек: %d' % left)


if __name__ == '__main__':
    main()
