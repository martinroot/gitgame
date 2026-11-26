#!/usr/bin/env python3
"""Restore catalog.json thumb paths for rated games whose JPEG already exists on the site."""
import json, os, shutil

CAT = '/var/www/fapa.io/dsgame/catalog/catalog.json'
RATINGS = '/var/www/fapa.io/dsgame/catalog/ratings.json'
THUMBS = '/var/www/gitgame.live/thumbs'
BACKUP = '/home/drogame/build/catalog_backups/catalog.json.before-thumb-repair'

os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
if not os.path.exists(BACKUP):
    shutil.copy2(CAT, BACKUP)
games = json.load(open(CAT))
ratings = json.load(open(RATINGS))
fixed = []
for g in games:
    slug = (g.get('slug') or '').strip()
    if slug not in ratings or g.get('thumb'):
        continue
    name = slug + '.jpg'
    if os.path.isfile(os.path.join(THUMBS, name)) and os.path.getsize(os.path.join(THUMBS, name)) > 1000:
        g['thumb'] = 'thumbs/' + name
        fixed.append(slug)
with open(CAT, 'w') as f:
    json.dump(games, f, ensure_ascii=False, indent=2)
print('restored thumb paths:', len(fixed))
print('sample:', fixed[:8])
