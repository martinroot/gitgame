#!/usr/bin/env python3
"""catalog_servercheck.py — authoritative check on the ACTUAL server (root-ssh).

For each card: whether the file {slug}/{path}index.html exists and what is in the folder.
One ssh call for everything (find), parsing is local. More accurate than HTTP: does not depend
on the nginx cache, network stuff, or the web server."""
import json
import os
import re
import subprocess

FAPA_PASS = os.environ.get('FAPA_PASS', '')
CAT = '/var/www/fapa.io/dsgame/catalog'


def ssh(cmd, t=240):
    return subprocess.run(
        ['sshpass', '-e', 'ssh', '-o', 'StrictHostKeyChecking=no', 'root@127.0.0.1', cmd],
        capture_output=True, text=True, timeout=t, env={**os.environ, 'SSHPASS': FAPA_PASS})


def main():
    with open(os.path.join(CAT, 'catalog.json'), encoding='utf-8') as fh:
        cat = json.load(fh)

    # One pass: all index.html files in the catalog + a list of all top-level folders
    out = ssh('find %s -maxdepth 4 -name index.html -printf "%%P\\n"' % CAT).stdout
    idx = set(out.split())
    out2 = ssh('find %s -mindepth 1 -maxdepth 1 -type d -printf "%%f\\n"' % CAT).stdout
    dirs = set(out2.split())
    out3 = ssh('for d in %s/*/; do n=$(find "$d" -type f 2>/dev/null | wc -l); '
               'echo "$(basename "$d") $n"; done' % CAT).stdout
    fcount = {}
    for line in out3.split('\n'):
        parts = line.split()
        if len(parts) == 2:
            fcount[parts[0]] = int(parts[1])

    res = []
    bad, empty = [], []
    for g in cat:
        slug = g.get('slug', '')
        path = (g.get('path') or '').strip('/')
        rel = f'{slug}/{path}index.html' if path else f'{slug}/index.html'
        r = {'slug': slug, 'path': path, 'files': fcount.get(slug, 0)}
        if slug not in dirs:
            r['why'] = 'no-dir'
            bad.append(r)
            continue
        if rel not in idx:
            # look for index.html elsewhere in the folder (only path may be broken)
            alts = sorted(x for x in idx if x.startswith(slug + '/') and x.endswith('index.html'))
            r['alts'] = alts[:3]
            r['why'] = 'no-index-at-path'
            bad.append(r)
            continue
        if r['files'] == 0:
            r['why'] = 'empty-dir'
            empty.append(r)
            continue
        r['why'] = 'ok'
        res.append(r)

    print('карточек: %d' % len(cat))
    print('OK (index.html на месте): %d' % len(res))
    print('НЕ ОК (index.html по path отсутствует): %d' % len(bad))
    for r in bad:
        print('   %-38s files=%-5d %s %s' % (r['slug'], r['files'], r['why'],
                                             ('alts=' + ','.join(r['alts'])) if r.get('alts') else ''))
    print('пустые папки (0 файлов): %d' % len(empty))
    for r in empty:
        print('   %-38s' % r['slug'])

    with open('/home/drogame/build/catalog_servercheck.json', 'w', encoding='utf-8') as fh:
        json.dump({'bad': bad, 'empty': empty, 'ok_count': len(res),
                   'dirs_unmarked': sorted(dirs - {g.get('slug') for g in cat} - {'thumbs'})},
                  fh, ensure_ascii=False, indent=1)
    print('\nнеразмеченные папки (нет карточки): %s'
          % sorted(dirs - {g.get('slug') for g in cat} - {'thumbs'}))


if __name__ == '__main__':
    main()
