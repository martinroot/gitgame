#!/usr/bin/env python3
"""
auto_deploy.py — автономный деплой найденных парсером игр в каталог на fapa.
Клон -> классификация -> сборка(Vite --base=./)/статика -> деплой на fapa
-> тест-рендер + игровой скрин -> карточка в catalog.json -> ссылка+скрин в Telegram.
Сложные (Next/Go/без root index.html/тяжёлые) пропускает с пометкой в ledger.

  python3 auto_deploy.py --n 8         # обработать до 8 новых кандидатов
  python3 auto_deploy.py --slugs a,b   # (не используется; авто по games.db)
"""
import argparse, base64, json, os, re, shutil, subprocess, sys, time
sys.path.insert(0, '/home/drogame/vibegame')
import game_crawler as gc

BUILD   = '/home/drogame/build'
CLONES  = f'{BUILD}/auto_clones'
STAGE   = '/home/drogame/build/deploy/catalog'      # локальный источник catalog.json
LEDGER  = f'{BUILD}/auto_deployed.txt'
FAPA_PASS = os.environ.get('FAPA_PASS', '')
FAPA_CAT  = '/var/www/fapa.io/dsgame/catalog'
PUB_BASE  = 'https://fapa.io/dsgame/catalog'
TG_CHAT   = '353169388'
CHROME = 'google-chrome-stable'

def sh(cmd, timeout=120, cwd=None):
    return subprocess.run(cmd, shell=True, cwd=cwd, timeout=timeout,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

def ssh_fapa(cmd, timeout=180):
    return sh(f"SSHPASS={FAPA_PASS} sshpass -e ssh -o StrictHostKeyChecking=no root@127.0.0.1 "
              + subprocess.list2cmdline([cmd]), timeout=timeout)

def scp_fapa(local, remote, timeout=300):
    return sh(f"SSHPASS={FAPA_PASS} sshpass -e scp -r -o StrictHostKeyChecking=no "
              f"{local} root@127.0.0.1:{remote}", timeout=timeout)

def fapa_catalog():
    """ЕДИНЫЙ источник правды — catalog.json на fapa (отражает удаления кнопкой 🗑)."""
    out = ssh_fapa(f'cat {FAPA_CAT}/catalog.json').stdout
    try:
        return json.loads(out) if out.strip() else []
    except Exception:
        return []

def catalog_add(entry):
    """Атомарно (flock) добавить карточку в fapa catalog.json, если слага/сорса ещё нет."""
    eb = base64.b64encode(json.dumps(entry, ensure_ascii=False).encode()).decode()
    php = ('<?php $f="%s/catalog.json"; $fh=fopen($f,"c+"); if(!$fh){echo "err";exit;} '
           'flock($fh,LOCK_EX); $c=json_decode(stream_get_contents($fh),true); if(!is_array($c))$c=[]; '
           '$e=json_decode(base64_decode("%s"),true); $ex=false; '
           'foreach($c as $g){ if(($g["slug"]??"")===$e["slug"]||($g["source"]??"")===$e["source"]){$ex=true;break;} } '
           'if(!$ex){ $c[]=$e; ftruncate($fh,0); rewind($fh); '
           'fwrite($fh,json_encode($c,JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT)); } '
           'flock($fh,LOCK_UN); fclose($fh); echo $ex?"exists":"added";') % (FAPA_CAT, eb)
    pb = base64.b64encode(php.encode()).decode()
    return ssh_fapa(f'echo {pb} | base64 -d | php').stdout.strip()

def ledger_load():
    return set(open(LEDGER).read().split()) if os.path.exists(LEDGER) else set()

def ledger_add(slug, status):
    with open(LEDGER, 'a') as f:
        f.write(f"{slug}\n")
    print(f"  ledger: {slug} = {status}", file=sys.stderr)

def tg_photo(path, caption):
    gc.load_env(gc.TG_ENV_PATH)
    tok = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not tok:
        return False
    import requests
    with open(path, 'rb') as f:
        r = requests.post(f"https://api.telegram.org/bot{tok}/sendPhoto", timeout=120,
                          data={'chat_id': TG_CHAT, 'caption': caption[:1024], 'parse_mode': 'HTML'},
                          files={'photo': f})
    return r.status_code == 200

def tg_text(text):
    gc.load_env(gc.TG_ENV_PATH)
    tok = os.environ.get('TELEGRAM_BOT_TOKEN')
    import requests
    requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", timeout=60,
                  data={'chat_id': TG_CHAT, 'text': text, 'parse_mode': 'HTML',
                        'disable_web_page_preview': 'true'})

def screenshot(url, dest, size='1000,720'):
    prof = f'/tmp/.cp{int(time.time()*1000)}'
    # timeout -k гарантированно убивает подвисший chrome (иначе копятся зомби-процессы)
    cmd = (f'timeout -k 5 50 {CHROME} --headless=new --disable-gpu --no-sandbox --disable-dev-shm-usage '
           f'--use-gl=angle --use-angle=swiftshader-webgl --enable-webgl --hide-scrollbars '
           f'--window-size={size} --force-device-scale-factor=1 --user-data-dir={prof} '
           f'--virtual-time-budget=9000 --screenshot={dest} "{url}"')
    try: sh(cmd, timeout=60)
    except Exception: pass
    sh(f'pkill -9 -f "user-data-dir={prof}" 2>/dev/null', timeout=10)
    shutil.rmtree(prof, ignore_errors=True)
    return os.path.exists(dest) and os.path.getsize(dest) > 5000

def thumb(src, dest):
    try:
        from PIL import Image
        im = Image.open(src).convert('RGB'); im.thumbnail((640, 640))
        im.save(dest, 'JPEG', quality=85); return True
    except Exception: return False

def find_index(root):
    for d in ['', 'dist', 'dist-client', 'build', 'out', 'public']:
        p = os.path.join(root, d, 'index.html') if d else os.path.join(root, 'index.html')
        if os.path.isfile(p): return os.path.dirname(p)
    hits = sh(f"find {root} -maxdepth 2 -name index.html -not -path '*/node_modules/*'").stdout.split()
    return os.path.dirname(hits[0]) if hits else None

def vite_build(root):
    """Пытаемся собрать Vite-проект с относительным base. Возвращает папку dist или None."""
    if not (os.path.exists(f'{root}/vite.config.ts') or os.path.exists(f'{root}/vite.config.js')
            or 'vite' in (open(f'{root}/package.json').read() if os.path.exists(f'{root}/package.json') else '')):
        return None
    env = 'export PATH="$HOME/.bun/bin:$PATH";'
    sh(f'{env} bun install', timeout=300, cwd=root)
    cfg = ''
    if os.path.exists(f'{root}/vite.standalone.ts'): cfg = '--config vite.standalone.ts'
    sh(f'{env} bun --bun ./node_modules/.bin/vite build --base=./ {cfg}', timeout=300, cwd=root)
    for d in ['dist-client', 'dist', 'build']:
        if os.path.isfile(f'{root}/{d}/index.html'): return f'{root}/{d}'
    return None

def deploy_one(r):
    full = r['full_name']; owner, name = full.split('/', 1)
    slug = re.sub(r'[^a-z0-9._-]+', '-', name.lower()).strip('-')
    cat = fapa_catalog()
    if any(g.get('slug') == slug or g.get('source') == r['html_url'] for g in cat):
        return 'exists'
    d = f'{CLONES}/{slug}'
    shutil.rmtree(d, ignore_errors=True)
    if sh(f'git clone --depth 1 https://github.com/{full} {d}', timeout=180).returncode != 0:
        return 'clone-fail'
    # размер
    szkb = int(sh(f"du -sk --exclude=.git {d}").stdout.split()[0] or 0)
    # артефакт: сборка Vite -> dist (subpath=''); статика -> корень репо + подпуть до index.html
    idx = find_index(d)
    needbuild = False
    if idx:
        html = open(f'{idx}/index.html', errors='ignore').read()
        needbuild = bool(re.search(r'src="/?src/|\.(tsx|jsx)"', html))
    if needbuild or (idx is None):
        dist = vite_build(d)
        if dist is None:
            return 'skip-build'      # Next/Go/Electron/непонятное — пропускаем
        deploy_src, subpath = dist, ''
    else:
        # статика: деплоим ВЕСЬ корень репо (чтобы не потерять ассеты вне папки index),
        # играбельный путь = подпапка с index.html
        deploy_src = d
        subpath = os.path.relpath(idx, d)
        if subpath == '.':
            subpath = ''
    if not os.path.isfile(os.path.join(deploy_src, subpath, 'index.html')):
        return 'no-index'
    srckb = int(sh(f"du -sk --exclude=.git {deploy_src}").stdout.split()[0] or 0)
    if srckb > 250000:
        return 'skip-too-big'
    playpath = f'{slug}/{subpath}/' if subpath else f'{slug}/'
    # rsync-исключения: НЕ выкидывать папку, в которой лежит игровой index.html
    # (иначе на сервере останется папка без игры -> битая карточка в каталоге).
    excludes = ['.git', 'node_modules', '.github']
    for junk in ('tests', 'docs'):
        # мусор выкидываем только если игровой index лежит не внутри него
        if not (subpath == junk or subpath.startswith(junk + '/')):
            excludes.append(junk)
    ex_args = ' '.join('--exclude=%s' % e for e in excludes)
    # деплой на fapa (rsync корня с исключениями мусора)
    ssh_fapa(f'rm -rf {FAPA_CAT}/{slug}')
    ssh_fapa(f'mkdir -p {FAPA_CAT}/{slug}')
    sh("SSHPASS=%s sshpass -e rsync -az --delete %s "
       "-e 'ssh -o StrictHostKeyChecking=no' %s/ root@127.0.0.1:%s/%s/"
       % (FAPA_PASS, ex_args, deploy_src, FAPA_CAT, slug), timeout=400)
    ssh_fapa(f'chown -R www-data:www-data {FAPA_CAT}/{slug}; find {FAPA_CAT}/{slug} -type d -exec chmod 755 {{}} +; '
             f'find {FAPA_CAT}/{slug} -type f -exec chmod 644 {{}} +')
    # ПРОВЕРКА на сервере: игра реально лежит по игровому пути? Если нет — сносим
    # папку и НЕ добавляем карточку (иначе в каталоге остаётся битая ссылка).
    chk = ssh_fapa(f'test -f {FAPA_CAT}/{slug}/{subpath}index.html && echo OK || echo MISSING').stdout.strip()
    if 'OK' not in chk:
        ssh_fapa(f'rm -rf {FAPA_CAT}/{slug}')
        print(f'  post-deploy check: {slug}/{subpath}index.html MISSING -> папка удалена, карточка не создана',
              file=sys.stderr)
        return 'no-index-on-server'
    # размер задеплоенной папки (человекочитаемо)
    try:
        gsize = (ssh_fapa(f'du -sh {FAPA_CAT}/{slug}').stdout.split() or [''])[0]
    except Exception:
        gsize = ''
    # скрин через публичный URL (с учётом подпути)
    shot = f'/tmp/ad_{slug}.png'
    ok_shot = screenshot(f'{PUB_BASE}/{playpath}', shot)
    thumb_ok = False
    if ok_shot:
        th = f'{STAGE}/thumbs/{slug}.jpg'
        thumb_ok = thumb(shot, th)
        if thumb_ok:
            scp_fapa(th, f'{FAPA_CAT}/thumbs/{slug}.jpg')
            ssh_fapa(f'chown www-data:www-data {FAPA_CAT}/thumbs/{slug}.jpg')
    # карточка в манифест (локально + на fapa)
    ai = 'AI' if gc.ai_signal(r) else ''
    entry = {'slug': slug, 'title': name.replace('-', ' ').replace('_', ' ').title(),
             'desc': (r['description'] or '').strip()[:200] or 'Игра из парсера, авто-деплой.',
             'tags': [t for t in [ai, r['engine'], ('demo' if r['demo'] else ''), f"⭐{r['stars']}"] if t],
             'thumb': f'thumbs/{slug}.jpg' if thumb_ok else '',
             'path': (subpath + '/' if subpath else ''),
             'size': gsize,
             'date': (r['created_at'] or '')[:10],
             'source': r['html_url']}
    catalog_add(entry)   # атомарно в fapa catalog.json (единый источник, под flock)
    # пост в телеграм
    cap = (f'🎮 <b>{gc.h(entry["title"])}</b>\n'
           f'⭐{r["stars"]} · {gc.days_since(r["created_at"])}д{" · 🤖AI" if ai else ""}'
           f'{" · "+r["engine"] if r["engine"] else ""}{" · 📦"+gsize if gsize else ""}\n'
           f'{gc.h(entry["desc"])}\n'
           f'▶️ играть: {PUB_BASE}/{playpath}\n'
           f'🔗 исходник: {r["html_url"]}')
    if ok_shot and thumb_ok:
        tg_photo(f'{STAGE}/thumbs/{slug}.jpg', cap)
    else:
        tg_text(cap + '\n(скрин не снялся — проверь вручную)')
    shutil.rmtree(d, ignore_errors=True)   # чистим клон (диск)
    return 'deployed'

# самые свежие топ-модели — по ним ГЛАВНЫЙ приоритет деплоя
FRESH_MODELS = ['gpt-6', 'gpt6', 'gpt 6', 'gpt-6-astra', 'astra', 'fable', 'claude fable',
                'fable 5', 'grok 4', 'grok4', 'grok-4', 'gemini 3', 'gemini-3', 'gemini3',
                'qwen3', 'qwen 3', 'qwen-3', 'deepseek v3', 'deepseek-v3', 'kimi k2', 'kimi-k2',
                'glm-4', 'glm 4', 'minimax', 'opus 4', 'sonnet 4', 'claude 4']

def _mboost(r):
    t = f"{r['full_name']} {r['description'] or ''} {r['topics'] or ''}".lower()
    return sum(1 for m in FRESH_MODELS if m in t)

def candidates(n, done):
    con = gc.db()
    rows = con.execute("SELECT * FROM repos WHERE scored=1 AND verdict!='junk'").fetchall()
    have_src = {g.get('source','') for g in fapa_catalog()}
    elig = []
    for r in rows:
        if not gc.is_game(r):
            continue
        if r['html_url'] in have_src:   # эта репа уже в каталоге под другим слагом
            continue
        # AI-ключи: только свежак (FRESH_DAYS); физ-ключи: горизонт ~90 дней
        is_phys = (r['src_query'] or '') in gc.PHYSICS_SET
        horizon = gc.PHYSICS_CUTOFF_DAYS if is_phys else gc.FRESH_DAYS
        if gc.days_since(r['created_at']) > horizon:
            continue
        slug = re.sub(r'[^a-z0-9._-]+', '-', r['full_name'].split('/', 1)[1].lower()).strip('-')
        if slug in done:
            continue
        elig.append(r)
    # приоритет: свежие топ-модели (gpt6/astra/fable…) вперёд, среди них — самые свежие по дате,
    # затем остальные по звёздам
    elig.sort(key=lambda r: (-_mboost(r), gc.days_since(r['created_at']), -(r['stars'] or 0)))
    return elig[:n]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--n', type=int, default=6)
    args = ap.parse_args()
    os.makedirs(CLONES, exist_ok=True)
    done = ledger_load()
    cat_slugs = {g.get('slug') for g in fapa_catalog()}
    done |= cat_slugs
    cands = candidates(args.n, done)
    print(f"кандидатов к деплою: {len(cands)}", file=sys.stderr)
    for r in cands:
        free_gb = shutil.disk_usage('/').free / 1e9
        if free_gb < 2.5:
            print(f"диск <2ГБ (свободно {free_gb:.1f}) — стоп волны", file=sys.stderr)
            tg_text('⚠️ Автодеплой на паузе: на сервере меньше 2 ГБ свободно. '
                    'Удали лишние игры кнопкой 🗑 — как освободится, деплой продолжится сам.')
            break
        slug = re.sub(r'[^a-z0-9._-]+', '-', r['full_name'].split('/', 1)[1].lower()).strip('-')
        print(f"[deploy] {r['full_name']} -> {slug}", file=sys.stderr)
        try:
            st = deploy_one(r)
        except Exception as e:
            st = f'error:{e}'
        ledger_add(slug, st)
        print(f"  => {st}", file=sys.stderr)
        time.sleep(1)

if __name__ == '__main__':
    main()
