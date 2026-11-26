#!/usr/bin/env python3
"""Детали по битым слагам: карточка + что реально лежит в папке."""
import json
import os
import subprocess

CAT = '/var/www/fapa.io/dsgame/catalog'
slugs = [s.strip() for s in open('/home/drogame/build/bad_slugs.txt') if s.strip()]
cat = {g['slug']: g for g in json.load(open(f'{CAT}/catalog.json'))}

for s in slugs:
    g = cat.get(s, {})
    p = os.path.join(CAT, s)
    print('=' * 70)
    print(s, '| path=%r' % g.get('path'), '| thumb=%r' % bool(g.get('thumb')))
    nfiles = 0
    total = 0
    top = []
    for root, dirs, files in os.walk(p):
        nfiles += len(files)
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
        if root.count(os.sep) - p.count(os.sep) < 1 and len(top) < 12:
            top.extend(sorted(os.listdir(root))[:12])
    print('  files=%d size=%.1fM' % (nfiles, total / 1048576))
    print('  top:', ', '.join(top[:12]))
    idxs = []
    for root, dirs, files in os.walk(p):
        if 'index.html' in files:
            idxs.append(os.path.relpath(root, p))
    print('  index.html в:', idxs[:5] if idxs else 'НЕТ')
