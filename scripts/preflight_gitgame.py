#!/usr/bin/env python3
"""Fail if any rated game in the catalog has no usable thumbnail."""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAT = Path(os.environ.get('CATALOG_JSON', '/var/www/fapa.io/dsgame/catalog/catalog.json'))
RATINGS = Path(os.environ.get('RATINGS_JSON', '/var/www/fapa.io/dsgame/catalog/ratings.json'))
THUMBS = Path(os.environ.get('SITE_THUMBS', '/var/www/gitgame.live'))


def check_thumbs(cat=CAT, ratings=RATINGS, thumbs=THUMBS):
    games = json.load(open(cat))
    scores = json.load(open(ratings))
    missing = []
    checked = 0
    for game in games:
        slug = (game.get('slug') or '').strip()
        if not slug or slug not in scores:
            continue
        checked += 1
        name = Path(game.get('thumb') or '').name or slug + '.jpg'
        if not (thumbs / 'thumbs' / name).exists() and (thumbs / 'thumbs' / (slug + '.jpg')).exists():
            name = slug + '.jpg'
        if not (thumbs / 'thumbs' / name).exists():
            missing.append(slug)
    return missing, checked


def main():
    missing, checked = check_thumbs()
    if missing:
        print('PREFLIGHT FAIL: missing thumbnails: ' + ', '.join(missing), file=sys.stderr)
        return 1
    print(f'PREFLIGHT OK: {checked} rated games, 0 missing thumbnails')
    return 0


if __name__ == '__main__':
    sys.exit(main())
