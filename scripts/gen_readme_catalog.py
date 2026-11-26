#!/usr/bin/env python3
"""Build README.md game catalog from the deployment catalog + manual ratings.

Sorting matches gitgame.live: stars desc, price desc, title asc.
Paths can be overridden with CATALOG_JSON / RATINGS_JSON / SITE_THUMBS env vars.
"""
import html
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAT = os.environ.get('CATALOG_JSON', '/var/www/fapa.io/dsgame/catalog/catalog.json')
RATINGS = os.environ.get('RATINGS_JSON', '/var/www/fapa.io/dsgame/catalog/ratings.json')
THUMBS = Path(os.environ.get('SITE_THUMBS', '/var/www/gitgame.live'))
PRICES = os.environ.get('PRICES_JSON', '/var/www/gitgame.live/api/prices.json')
SITE = 'https://gitgame.live'


def short(text, limit=70):
    text = html.unescape(re.sub(r'<[^>]+>', ' ', text or '')).replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text).replace('|', '/')
    if len(text) > limit:
        text = text[:limit].rsplit(' ', 1)[0] + '…'
    return text or 'HTML5-игра с исходниками.'


def main():
    games = json.load(open(CAT))
    ratings = json.load(open(RATINGS)) if os.path.exists(RATINGS) else {}
    prices = json.load(open(PRICES)) if os.path.exists(PRICES) else {}
    rows = []
    for g in games:
        slug = (g.get('slug') or '').strip()
        if not slug or slug not in ratings:
            continue
        stars = max(0, min(5, int(ratings[slug])))
        price = float(prices.get(slug, {5: 1.50, 4: 1.00, 3: 0.70, 2: 0.30, 1: 0.10}.get(stars, 0.30)))
        thumb = g.get('thumb') or ''
        thumb_name = Path(thumb).name if thumb else ''
        image = f'{SITE}/thumbs/{thumb_name}' if thumb_name and (THUMBS / 'thumbs' / thumb_name).exists() else None
        rows.append((stars, price, g.get('title') or slug, slug, short(g.get('desc')),
                     g.get('source') or '', image))
    rows.sort(key=lambda r: (-r[0], -r[1], r[2]))

    out = [
        '# GitGame',
        '',
        'Каталог HTML5-игр с готовыми веб-сборками и исходниками. Сайт: https://gitgame.live',
        '',
        f'**{len(rows)} игр** с ручной оценкой. Сортировка как на сайте: по звёздам, затем по цене и названию.',
        '',
        '## Каталог игр',
        '',
        '| | | | |',
        '|---|---|---|---|',
    ]
    cells = []
    for stars, price, title, slug, desc, source, image in rows:
        name = html.escape(title.replace('|', '/'))
        img = f'<img src="{image}" width="150" alt="{name}"><br>' if image else ''
        links = f'[▶]({SITE}/game/{slug}/)'
        if source.startswith('https://github.com/'):
            links += f' · [GitHub]({source})'
        cells.append(f'{img}<b>{"★" * stars}{"☆" * (5 - stars)} {name}</b><br>{desc}<br>{links}')
        if len(cells) == 4:
            out.append('| ' + ' | '.join(cells) + ' |')
            cells = []
    if cells:
        out.append('| ' + ' | '.join(cells + [''] * (4 - len(cells))) + ' |')
    (ROOT / 'README.md').write_text('\n'.join(out) + '\n')
    print(f'README.md: {len(rows)} games')


if __name__ == '__main__':
    main()
