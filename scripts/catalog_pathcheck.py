#!/usr/bin/env python3
"""
catalog_pathcheck.py — ищет карточки, у которых path указывает не туда.

Класс A: path в карточке не содержит index.html, но index.html есть в другом
         месте папки -> витрина ведёт в 404, хотя игра в папке есть (чинится).
Класс B: index.html нет нигде в папке -> игра действительно не задеплоена (снос).
"""
import json
import os

CAT = '/var/www/fapa.io/dsgame/catalog'
cat = json.load(open(f'{CAT}/catalog.json'))

fixable = []
hopeless = []
for g in cat:
    slug = g.get('slug', '')
    path = (g.get('path') or '').strip('/')
    base = os.path.join(CAT, slug)
    if not os.path.isdir(base):
        hopeless.append((slug, 'no-dir'))
        continue
    cur = os.path.join(base, path) if path else base
    if os.path.isfile(os.path.join(cur, 'index.html')):
        continue
    # ищем альтернативы
    alts = []
    for root, dirs, files in os.walk(base):
        if 'index.html' in files:
            alts.append(os.path.relpath(root, base))
    if alts:
        # ближайший к корню
        alts.sort(key=lambda a: (a.count(os.sep), len(a)))
        fixable.append((slug, path, alts[0], len(alts)))
    else:
        hopeless.append((slug, 'no-index-anywhere'))

print('=== ЧИНИТСЯ (path поправить): %d' % len(fixable))
for slug, path, alt, n in fixable:
    print('   %-38s path=%-14r -> %r (%d вариантов)' % (slug, path, alt, n))

print('\n=== НЕ ЧИНИТСЯ (index.html нет нигде): %d' % len(hopeless))
for slug, why in hopeless:
    n = 0
    tot = 0
    p = os.path.join(CAT, slug)
    for root, dirs, files in os.walk(p):
        n += len(files)
        for f in files:
            try:
                tot += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    print('   %-38s %-16s files=%-4d size=%.1fM' % (slug, why, n, tot / 1048576))
