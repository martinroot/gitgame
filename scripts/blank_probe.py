#!/usr/bin/env python3
"""
blank_probe.py — ручная проверка «blank»-игр: грузим страницу и смотрим,
что реально в DOM (текст, canvas, кнопка старта) вместо сухой картинки.

Для каждого слага: скрин + размер + доля тёмного + первые строки body.
"""
import os
import re
import subprocess
import sys
import time

PUB = 'https://fapa.io/dsgame/catalog'
CHROME = 'google-chrome-stable'
CAT = '/var/www/fapa.io/dsgame/catalog'

try:
    _CAT = {g['slug']: (g.get('path') or '') for g in json.load(open(f'{CAT}/catalog.json'))}
except Exception:
    _CAT = {}


def probe(slug, path=None):
    if path is None:
        path = _CAT.get(slug, '')
    url = f'{PUB}/{slug}/{path}' if path else f'{PUB}/{slug}/'
    prof = f'/tmp/.bp{int(time.time() * 1000)}'
    png = f'/tmp/bp_{slug}.png'
    dom = f'/tmp/bp_{slug}.html'
    err = f'/tmp/bp_{slug}.err'
    cmd = (f'timeout -k 5 50 {CHROME} --headless=new --disable-gpu --no-sandbox '
           f'--disable-dev-shm-usage --use-gl=angle --use-angle=swiftshader-webgl '
           f'--enable-webgl --hide-scrollbars --window-size=900,600 '
           f'--user-data-dir={prof} --enable-logging=stderr --log-level=0 '
           f'--virtual-time-budget=12000 --dump-dom "{url}" >{dom} 2>{err}')
    try:
        subprocess.run(cmd, shell=True, timeout=80, stdout=subprocess.DEVNULL)
    except Exception:
        pass
    subprocess.run(f'pkill -9 -f "user-data-dir={prof}" 2>/dev/null', shell=True)
    subprocess.run(f'rm -rf {prof}', shell=True)

    size = os.path.getsize(png) if os.path.exists(png) else 0
    body = ''
    if os.path.exists(dom):
        txt = open(dom, errors='ignore').read()
        body = re.sub(r'<[^>]+>', ' ', txt)
        body = re.sub(r'\s+', ' ', body).strip()
    js = ''
    if os.path.exists(err):
        e = open(err, errors='ignore').read()
        hits = [ln for ln in e.split('\n')
                if 'ERROR:CONSOLE' in ln or 'net::ERR' in ln]
        js = ' | '.join(h[:150] for h in hits[:3])
    has_canvas = 'canvas' in (open(dom, errors='ignore').read() if os.path.exists(dom) else '')
    return {'slug': slug, 'url': url, 'dom_bytes': os.path.getsize(dom) if os.path.exists(dom) else 0,
            'text': body[:200], 'js': js, 'canvas': has_canvas}


if __name__ == '__main__':
    slugs = [s.strip() for s in open(sys.argv[1]) if s.strip()]
    for s in slugs:
        r = probe(s)
        print('--- %s' % r['slug'])
        print('    dom=%dB canvas=%s' % (r['dom_bytes'], r['canvas']))
        print('    text: %s' % r['text'][:160])
        if r['js']:
            print('    js:   %s' % r['js'])
