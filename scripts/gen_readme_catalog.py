#!/usr/bin/env python3
"""Build README.md game catalog from the deployment catalog and manual ratings.

Sorting matches gitgame.live: stars desc, price desc, title asc.
Russian descriptions are replaced by translations from data/descriptions_en.json.
Paths can be overridden with CATALOG_JSON / RATINGS_JSON / SITE_THUMBS / PRICES_JSON.
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
    return text or 'HTML5 game with source code.'


def image_url(slug, thumb, thumbs=THUMBS):
    """Resolve a game image: explicit catalog path, then <slug>.jpg, else None."""
    name = Path(thumb).name if thumb else ''
    candidates = [name] if name else []
    candidates.append(slug + '.jpg')
    for candidate in candidates:
        path = thumbs / 'thumbs' / candidate
        if path.exists():
            return f'{SITE}/thumbs/{candidate}'
    return None


def main():
    games = json.load(open(CAT))
    ratings = json.load(open(RATINGS)) if os.path.exists(RATINGS) else {}
    prices = json.load(open(PRICES)) if os.path.exists(PRICES) else {}
    en_desc = json.load(open(ROOT / 'data/descriptions_en.json'))
    rows = []
    missing = []
    for g in games:
        slug = (g.get('slug') or '').strip()
        if not slug or slug not in ratings:
            continue
        stars = max(0, min(5, int(ratings[slug])))
        price = float(prices.get(slug, {5: 1.50, 4: 1.00, 3: 0.70, 2: 0.30, 1: 0.10}.get(stars, 0.30)))
        image = image_url(slug, g.get('thumb') or '', THUMBS)
        if image is None:
            missing.append(slug)
        desc = en_desc.get(slug) or g.get('desc') or ''
        rows.append((stars, price, g.get('title') or slug, slug, short(desc),
                     g.get('source') or '', image))
    if missing:
        raise SystemExit('missing thumbnails: ' + ', '.join(missing))
    rows.sort(key=lambda r: (-r[0], -r[1], r[2]))

    out = [
        '# GitGame',
        '',
        'A catalog of HTML5 games with ready web builds and source code. Live site: https://gitgame.live',
        '',
        f'**{len(rows)} rated games**, sorted like the site: by stars, then price and title.',
        '',
        '## Scripts',
        '',
        '- `scripts/game_crawler.py` — discover and enrich GitHub games (`--discover`, `--enrich`); SQLite DB `games.db`',
        '- `scripts/auto_deploy.py` — clone, build, deploy to the fapa.io/dsgame catalog (`--n 20`)',
        '- `scripts/daily.sh` — daily cycle: discover → enrich → deploy (cron 09:30)',
        '- `scripts/junk_purge.py`, `scripts/catalog_*.py` — catalog cleanup and checks (headless Chrome)',
        '- `scripts/gitgame_gen.py` — gitgame.live storefront generator (EN/DE/KR/RU/AR)',
        '- `scripts/gen_gitgame_prices.py` — export catalog prices to `api/prices.json` for checkout',
        '- `web/api/*.php` — DV-merchant crypto billing: cart checkout, webhook, order status, account recovery and paid source downloads',
        '- `scripts/gen_readme_catalog.py` — regenerate this README from catalog data',
        '- `scripts/repair_catalog_thumbs.py` — restore missing catalog thumb paths from site JPEGs',
        '',
        'Regenerate with `python3 scripts/gen_readme_catalog.py`. Paths can be overridden via `CATALOG_JSON`, `RATINGS_JSON`, `PRICES_JSON`, `SITE_THUMBS`. Secrets come from the environment (`FAPA_PASS`, `GITHUB_TOKEN`) and are not stored in this repo.',
        '',
        '## Game catalog',
        '',
        '| | | |',
        '|---|---|---|',
    ]
    group = []
    for stars, price, title, slug, desc, source, image in rows:
        name = html.escape(title.replace('|', '/'))
        img = (f'<img src="{image}" width="200" height="120" alt="{name}">'
               if image else '<sub>No preview</sub>')
        links = f'[Play]({SITE}/game/{slug}/)'
        if source.startswith('https://github.com/'):
            links += f' · [GitHub]({source})'
        group.append((img, f'<b>{"★" * stars}{"☆" * (5 - stars)} {name}</b><br>{desc}<br>{links}'))
        if len(group) == 3:
            out.append('| ' + ' | '.join(x[0] for x in group) + ' |')
            out.append('| ' + ' | '.join(x[1] for x in group) + ' |')
            group = []
    if group:
        group += [('', '')] * (3 - len(group))
        out.append('| ' + ' | '.join(x[0] for x in group) + ' |')
        out.append('| ' + ' | '.join(x[1] for x in group) + ' |')
    (ROOT / 'README.md').write_text('\n'.join(out) + '\n')
    print(f'README.md: {len(rows)} games')


if __name__ == '__main__':
    main()
