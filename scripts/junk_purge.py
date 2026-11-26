#!/usr/bin/env python3
"""
junk_purge.py — авто-отсев шлака: свежий ре-рендер каждой игры каталога.
Битой считается игра, у которой скрин ПУСТОЙ (почти однотонный = не отрисовалась)
ИЛИ есть фатальная JS-ошибка в консоли. Такие удаляются из каталога (catalog.json + папка + превью).

  python3 junk_purge.py --dry [--limit N]   # только показать, что попадёт под нож
  python3 junk_purge.py                      # реально удалить битые
"""
import argparse, base64, json, os, re, subprocess, sys, time
from collections import Counter
from PIL import Image

FAPA_PASS = os.environ.get('FAPA_PASS', '')
FAPA_CAT  = '/var/www/fapa.io/dsgame/catalog'
PUB       = 'https://fapa.io/dsgame/catalog'
TG_CHAT   = '353169388'
sys.path.insert(0, '/home/drogame/vibegame'); import game_crawler as gc

def ssh(cmd, t=180):
    return subprocess.run(['sshpass', '-e', 'ssh', '-o', 'StrictHostKeyChecking=no', 'root@127.0.0.1', cmd],
                          capture_output=True, text=True, timeout=t,
                          env={**os.environ, 'SSHPASS': FAPA_PASS})

def catalog():
    try:
        return json.loads(ssh(f'cat {FAPA_CAT}/catalog.json').stdout or '[]')
    except Exception:
        return []

def tg(text):
    gc.load_env(gc.TG_ENV_PATH); import requests
    tok = os.environ.get('TELEGRAM_BOT_TOKEN')
    if tok:
        requests.post(f'https://api.telegram.org/bot{tok}/sendMessage', timeout=60,
                      data={'chat_id': TG_CHAT, 'text': text, 'parse_mode': 'HTML',
                            'disable_web_page_preview': 'true'})

JS_ERR = re.compile(r'ERROR:CONSOLE.*(Uncaught|is not defined|SyntaxError|ReferenceError|TypeError)', re.I)

def is_blank(png):
    try:
        im = Image.open(png).convert('RGB'); im.thumbnail((120, 120))
        px = list(im.getdata()); n = len(px)
        g = [(r*299+gr*587+b*114)//1000 for r, gr, b in px]
        m = sum(g)/n; std = (sum((x-m)**2 for x in g)/n)**0.5
        dom = Counter((r>>4, gr>>4, b>>4) for r, gr, b in px).most_common(1)[0][1]/n
        # СТРОГО: только по-настоящему пустая страница (почти один цвет), чтобы не задеть
        # тёмные игры и «клик-чтобы-старт» (у них тёмный, но не однотонный кадр)
        return (std < 4.5 and dom > 0.95), round(std, 1), round(dom, 2)
    except Exception:
        return None, 0, 0

def check(g):
    """Возвращает (broken:bool, reason:str)."""
    slug = g['slug']; path = g.get('path', '')
    url = f'{PUB}/{slug}/{path}'
    prof = f'/tmp/.jp{os.getpid()}_{int(time.time()*1000)}'
    png = f'/tmp/jp_{slug}.png'; err = f'/tmp/jp_{slug}.err'
    cmd = (f'timeout -k 5 45 google-chrome-stable --headless=new --disable-gpu --no-sandbox '
           f'--disable-dev-shm-usage --use-gl=angle --use-angle=swiftshader-webgl --enable-webgl '
           f'--hide-scrollbars --window-size=900,600 --user-data-dir={prof} '
           f'--enable-logging=stderr --log-level=0 --virtual-time-budget=10000 '
           f'--screenshot={png} "{url}" 2>{err}')
    try:
        subprocess.run(cmd, shell=True, timeout=70, stdout=subprocess.DEVNULL)
    except Exception:
        pass
    subprocess.run(f'pkill -9 -f "user-data-dir={prof}" 2>/dev/null', shell=True)
    subprocess.run(f'rm -rf {prof}', shell=True)
    broken, reason = False, 'ok'
    if not (os.path.exists(png) and os.path.getsize(png) > 2000):
        reason = 'no-shot'          # ничего не отрисовалось — не удаляем (может транзиент)
    else:
        bl, std, dom = is_blank(png)
        if bl:
            broken, reason = True, f'blank(std={std},dom={dom})'
        else:
            try:
                errtxt = open(err, errors='ignore').read()
                if JS_ERR.search(errtxt):
                    broken, reason = True, 'js-error'
            except Exception:
                pass
    for f in (png, err):
        try: os.remove(f)
        except OSError: pass
    return broken, reason

def purge(slugs):
    """Удалить список слагов из fapa catalog.json (flock) + папки + превью."""
    sb = base64.b64encode(json.dumps(slugs).encode()).decode()
    php = ('<?php $dir="%s"; $f="$dir/catalog.json"; $fh=fopen($f,"c+"); flock($fh,LOCK_EX); '
           '$c=json_decode(stream_get_contents($fh),true); if(!is_array($c))$c=[]; '
           '$rm=json_decode(base64_decode("%s"),true); $set=array_flip($rm); '
           '$c=array_values(array_filter($c,fn($g)=>!isset($set[$g["slug"]??""]))); '
           'ftruncate($fh,0); rewind($fh); fwrite($fh,json_encode($c,JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT)); '
           'flock($fh,LOCK_UN); fclose($fh); '
           'function rr($p){ if(is_file($p)||is_link($p)){@unlink($p);return;} if(!is_dir($p))return; '
           'foreach(scandir($p) as $e){ if($e=="."||$e=="..")continue; rr("$p/$e"); } @rmdir($p);} '
           '$base=realpath($dir); foreach($rm as $s){ if(!preg_match("/^[A-Za-z0-9._-]+$/",$s))continue; '
           '$gd=realpath("$dir/$s"); if($gd&&strpos($gd,$base.DIRECTORY_SEPARATOR)===0) rr($gd); '
           '@unlink("$dir/thumbs/$s.jpg"); } echo "removed=".count($rm);') % (FAPA_CAT, sb)
    pb = base64.b64encode(php.encode()).decode()
    return ssh(f'echo {pb} | base64 -d | php').stdout.strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--batch', type=int, default=25, help='удалять пачками по N')
    args = ap.parse_args()

    games = catalog()
    if args.limit:
        games = games[:args.limit]
    total = len(games)
    print(f'проверяю {total} игр (dry={args.dry})', file=sys.stderr)
    if not args.dry:
        tg(f'🧹 Авто-отсев шлака запущен: проверяю {total} игр (пустой рендер + JS-ошибки), битые удаляю.')

    from concurrent.futures import ThreadPoolExecutor, as_completed
    broken, pending = [], []
    done = 0
    def work(g):
        try:
            return g, check(g)
        except Exception as e:
            return g, (False, f'err:{e}')
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = [ex.submit(work, g) for g in games]
        for fu in as_completed(futs):
            g, (b, reason) = fu.result()
            done += 1
            print(f'[{done}/{total}] {"🔴 БИТАЯ" if b else "ok"} {g["slug"]} ({reason})', file=sys.stderr)
            if b:
                broken.append((g['slug'], reason)); pending.append(g['slug'])
            if not args.dry and len(pending) >= args.batch:
                print('  ', purge(pending), file=sys.stderr); pending = []
    if not args.dry and pending:
        print('  ', purge(pending), file=sys.stderr)

    print(f'\nИТОГО битых: {len(broken)} из {total}', file=sys.stderr)
    if args.dry:
        for s, r in broken[:60]:
            print(f'  {s}  [{r}]', file=sys.stderr)
    else:
        left = len(catalog())
        tg(f'🧹 Готово: удалено {len(broken)} битых игр из {total}. В каталоге осталось {left}.\n'
           f'(критерий: пустой/не отрисовавшийся скрин или JS-ошибка загрузки)')

if __name__ == '__main__':
    main()
