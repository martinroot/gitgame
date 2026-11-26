#!/usr/bin/env python3
"""catalog_verify.py — check of the fapa.io/dsgame/catalog catalog for loadability.

Levels (from cheapest to most expensive):
  1) static  — whether index.html exists at card['path']; whether the local
                resources referenced by index.html (src/href/url()) exist;
  2) http    — GET of the game URL: response code, size, final URL (redirect to a 404);
  3) render  — headless Chrome: JS errors in the console + an empty (solid-color) screenshot.

Output: JSON report + summary to stdout. Deletes nothing.

  python3 catalog_verify.py --level static|http|render --out report.json
  python3 catalog_verify.py --level http --limit 50 --slug foo,bar"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse

CAT = '/var/www/fapa.io/dsgame/catalog'
PUB = 'https://fapa.io/dsgame/catalog'
CHROME = 'google-chrome-stable'

# Local resources: relative or site-root-relative. External (http/https//) ones are not checked.
ATTR_RE = re.compile(
    r'''(?:src|href)\s*=\s*["']([^"']+)["']|url\(\s*["']?([^"')]+)["']?\s*\)''',
    re.I,
)
JS_ERR_RE = re.compile(
    r'ERROR:CONSOLE.*(?:Uncaught|SyntaxError|ReferenceError|TypeError|is not defined|'
    r'Failed to load module|net::ERR)', re.I)
NET_ERR_RE = re.compile(r'net::ERR_[A-Z_]+', re.I)


def catalog():
    with open(os.path.join(CAT, 'catalog.json'), encoding='utf-8') as fh:
        return json.load(fh)


def local_refs(html):
    """Local links from HTML: absolute from the site root and relative."""
    out = []
    for m in ATTR_RE.finditer(html):
        ref = (m.group(1) or m.group(2) or '').strip()
        if not ref or ref.startswith(('#', 'data:', 'mailto:', 'javascript:', 'blob:')):
            continue
        if re.match(r'^(?:https?:)?//', ref, re.I):
            continue
        out.append(ref.split('#')[0].split('?')[0])
    return out


def check_static(g):
    """Card -> game folder -> index.html -> local resources."""
    slug = g.get('slug', '')
    path = (g.get('path') or '').strip('/')
    base = os.path.join(CAT, slug)
    idx_dir = os.path.join(base, path) if path else base
    idx = os.path.join(idx_dir, 'index.html')
    res = {'slug': slug, 'problems': [], 'missing': [], 'checked_refs': 0}
    if not os.path.isdir(base):
        res['problems'].append('no-dir')
        return res
    if not os.path.isfile(idx):
        res['problems'].append('no-index')
        return res
    try:
        html = open(idx, encoding='utf-8', errors='ignore').read()
    except Exception as exc:
        res['problems'].append('index-unreadable')
        res['detail'] = str(exc)
        return res
    res['index_bytes'] = len(html)
    if not html.strip():
        res['problems'].append('empty-index')
        return res
    for ref in local_refs(html):
        res['checked_refs'] += 1
        if ref.startswith('/'):
            # from the site root: /assets/... -> /var/www/fapa.io/assets/...
            cand = os.path.join('/var/www/fapa.io', ref.lstrip('/'))
        else:
            cand = os.path.join(idx_dir, ref)
        if not os.path.exists(cand):
            res['missing'].append(ref)
    if res['missing']:
        res['problems'].append('missing-assets')
    return res


def check_http(g):
    """GET of the game URL: code, size, redirect."""
    slug = g.get('slug', '')
    path = (g.get('path') or '').strip('/')
    url = f'{PUB}/{slug}/{path}' if path else f'{PUB}/{slug}/'
    res = {'slug': slug, 'url': url, 'problems': []}
    try:
        out = subprocess.run(
            ['curl', '-sS', '-o', '/dev/null', '-L', '--max-time', '25',
             '-w', '%{http_code} %{size_download} %{url_effective}', url],
            capture_output=True, text=True, timeout=40)
    except Exception as exc:
        res['problems'].append('curl-failed')
        res['detail'] = str(exc)
        return res
    parts = (out.stdout or '').strip().split()
    if len(parts) < 3:
        res['problems'].append('curl-no-output')
        return res
    code, size, final = parts[0], parts[1], parts[2]
    res['code'] = code
    res['size'] = int(size or 0)
    res['final'] = final
    if code != '200':
        res['problems'].append(f'http-{code}')
    elif int(size or 0) < 200:
        res['problems'].append('empty-body')
    if final.rstrip('/').endswith('/404.html') or '404' in final.lower():
        res['problems'].append('redirected-to-404')
    return res


def is_blank(png):
    """Empty frame = almost a single color (as in junk_purge.py)."""
    try:
        from PIL import Image
        from collections import Counter
        im = Image.open(png).convert('RGB')
        im.thumbnail((120, 120))
        px = list(im.getdata())
        n = len(px)
        g = [(r * 299 + gr * 587 + b * 114) // 1000 for r, gr, b in px]
        m = sum(g) / n
        std = (sum((x - m) ** 2 for x in g) / n) ** 0.5
        dom = Counter((r >> 4, gr >> 4, b >> 4) for r, gr, b in px).most_common(1)[0][1] / n
        return (std < 4.5 and dom > 0.95), round(std, 1), round(dom, 2)
    except Exception:
        return None, 0, 0


def check_render(g):
    """Headless Chrome: JS errors + blank screenshot."""
    slug = g.get('slug', '')
    path = (g.get('path') or '').strip('/')
    url = f'{PUB}/{slug}/{path}' if path else f'{PUB}/{slug}/'
    prof = f'/tmp/.cv{os.getpid()}_{int(time.time() * 1000)}'
    png = f'/tmp/cv_{slug}.png'
    err = f'/tmp/cv_{slug}.err'
    cmd = (f'timeout -k 5 45 {CHROME} --headless=new --disable-gpu --no-sandbox '
           f'--disable-dev-shm-usage --use-gl=angle --use-angle=swiftshader-webgl '
           f'--enable-webgl --hide-scrollbars --window-size=900,600 '
           f'--user-data-dir={prof} --enable-logging=stderr --log-level=0 '
           f'--virtual-time-budget=10000 --screenshot={png} "{url}" 2>{err}')
    res = {'slug': slug, 'problems': []}
    try:
        subprocess.run(cmd, shell=True, timeout=70, stdout=subprocess.DEVNULL)
    except Exception:
        res['problems'].append('chrome-timeout')
    subprocess.run(f'pkill -9 -f "user-data-dir={prof}" 2>/dev/null', shell=True)
    subprocess.run(f'rm -rf {prof}', shell=True)
    if not (os.path.exists(png) and os.path.getsize(png) > 2000):
        res['problems'].append('no-shot')
    else:
        bl, std, dom = is_blank(png)
        if bl:
            res['problems'].append(f'blank(std={std},dom={dom})')
    try:
        txt = open(err, errors='ignore').read()
        if JS_ERR_RE.search(txt):
            res['problems'].append('js-error')
            m = JS_ERR_RE.search(txt)
            res['detail'] = txt[max(0, m.start() - 120):m.start() + 260].replace('\n', ' ')
        elif NET_ERR_RE.search(txt):
            m = NET_ERR_RE.search(txt)
            res['problems'].append('net-error')
            res['detail'] = txt[max(0, m.start() - 120):m.start() + 200].replace('\n', ' ')
    except Exception:
        pass
    for f in (png, err):
        try:
            os.remove(f)
        except OSError:
            pass
    return res


LEVELS = {'static': check_static, 'http': check_http, 'render': check_render}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--level', choices=list(LEVELS), default='static')
    ap.add_argument('--out', default='')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--slug', default='')
    ap.add_argument('--workers', type=int, default=6)
    ap.add_argument('--resume', action='store_true',
                    help='не проверять заново слаги, уже успешно проверенные в --out')
    ap.add_argument('--only-good', action='store_true',
                    help='оставить только те, кто не помечен битым в предыдущем отчёте')
    args = ap.parse_args()

    games = catalog()
    if args.slug:
        want = {s.strip() for s in args.slug.split(',') if s.strip()}
        games = [g for g in games if g.get('slug') in want]
    if args.limit:
        games = games[:args.limit]

    prev = []
    if args.out and os.path.isfile(args.out):
        try:
            with open(args.out, encoding='utf-8') as fh:
                prev = json.load(fh).get('results', [])
        except Exception:
            prev = []
    prev_by_slug = {r.get('slug'): r for r in prev}
    if args.only_good:
        games = [g for g in games
                 if not (prev_by_slug.get(g.get('slug'), {}).get('problems'))]
    if args.resume:
        games = [g for g in games
                 if not (prev_by_slug.get(g.get('slug'), {}) or {}).get('problems')]

    fn = LEVELS[args.level]
    t0 = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(fn, g): g for g in games}
        for i, fu in enumerate(as_completed(futs), 1):
            g = futs[fu]
            try:
                r = fu.result()
            except Exception as exc:
                r = {'slug': g.get('slug', ''), 'problems': ['checker-failed'], 'detail': str(exc)}
            r['title'] = g.get('title', '')
            results.append(r)
            if i % 25 == 0 or i == len(games):
                bad = sum(1 for x in results if x.get('problems'))
                print('[%d/%d] bad=%d  %.0fs' % (i, len(games), bad, time.time() - t0),
                      file=sys.stderr, flush=True)

    results.sort(key=lambda r: r.get('slug', ''))
    if prev:
        merged = {r.get('slug'): r for r in prev}
        merged.update({r.get('slug'): r for r in results})
        results = list(merged.values())
        results.sort(key=lambda r: r.get('slug', ''))
    bad = [r for r in results if r.get('problems')]
    print('\n=== level=%s checked=%d bad=%d  (%.0fs)' % (args.level, len(results), len(bad), time.time() - t0))
    from collections import Counter
    reasons = Counter(p.split('(')[0] for r in bad for p in r.get('problems', []))
    for reason, n in reasons.most_common():
        print('   %-22s %d' % (reason, n))
    print('\n--- список битых ---')
    for r in bad:
        miss = r.get('missing') or []
        extra = (' missing=' + ','.join(miss[:3])) if miss else ''
        det = (' | ' + str(r.get('detail'))[:200]) if r.get('detail') else ''
        print('%-40s %-28s%s%s' % (r.get('slug', ''), ','.join(r.get('problems', [])),
                                   extra, det))
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as fh:
            json.dump({'level': args.level, 'checked': len(results),
                       'bad': len(bad), 'results': results}, fh, ensure_ascii=False, indent=1)
        print('\nreport: %s' % args.out)


if __name__ == '__main__':
    main()
