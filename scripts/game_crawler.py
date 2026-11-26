#!/usr/bin/env python3
"""
game_crawler.py — автономный краулер хайповых игровых репозиториев GitHub
для отбора под Яндекс.Игры. Пишет большую постоянную базу (SQLite),
обходит пространство поиска шардами (тема × недельное окно created),
работает порциями в рамках бюджета rate-limit и ставится на крон.

Стадии (разведены, каждая ограничена бюджетом):
  discovery  — sharded search API: находим репы, снапшотим звёзды
  enrich     — core API: лицензия/языки/файлы/README → fitness + demo + media
  digest     — шлём НОВЫЕ находки в Telegram (repo + demo + media)

Крон (чистый Python, без Claude → LLM-токенов 0):
  17 * * * *  python3 /home/drogame/vibegame/game_crawler.py --run
  30 9 * * *  python3 /home/drogame/vibegame/game_crawler.py --digest

CLI:
  python3 game_crawler.py --run        # ensure-shards + discovery + enrich (бюджетно)
  python3 game_crawler.py --discover   # только discovery
  python3 game_crawler.py --enrich     # только enrich
  python3 game_crawler.py --digest     # дайджест в Telegram
  python3 game_crawler.py --status     # статистика базы
"""

import argparse
import base64
import fcntl
import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timedelta, timezone

import requests

# ---------------------------------------------------------------- config
HOME = "/home/drogame/vibegame"
DB_PATH = os.path.join(HOME, "games.db")
ENV_PATH = os.path.join(HOME, ".env")
SHOTS_DIR = os.path.join(HOME, "shots")
CHROME = "google-chrome-stable"
TG_ENV_PATH = "/home/drogame/.claude/channels/telegram/.env"
TG_CHAT_ID = "353169388"

API = "https://api.github.com"

MONTHS_BACK = 2          # (устар.) не используется
CUTOFF_DAYS = 4          # НОВЫЙ ПРИНЦИП: ищем только за последние N дней
PHYSICS_CUTOFF_DAYS = 90 # для физ-ключей ограничение по дате снято: смотрим ~2-3 месяца
MIN_STARS = 0            # звёзды больше НЕ критерий — берём и свежак с 0 звёзд
PER_PAGE = 100
MAX_PAGES = 10           # жёсткий потолок Search API = 1000 результатов/запрос

# бюджет на один прогон
SEARCH_CALLS_PER_RUN = 60
ENRICH_REPOS_PER_RUN = 1500   # верхний кап; реально ограничит core-бюджет (~1700 реп/час)
SEARCH_FLOOR = 6         # стоп, если осталось меньше запросов поиска
CORE_FLOOR = 600         # стоп, если осталось меньше core-запросов
SEARCH_PACE = 2.0        # сек между search-запросами (лимит 30/мин)
CORE_PACE = 0.25

# дайджест
DIGEST_MIN_FITNESS = 60
DIGEST_MAX = 10          # потолок при ручном --digest
REALTIME_MAX = 6         # сколько постим за один автопрогон (realtime, остальное — в след. прогон)
# хайп-гейт: постим, только если у репы реальная тяга
HYPE_STARS = 50          # (устар.) хайп-порог, больше не гейт — оставлен для справки
HYPE_VELOCITY = 4.0      # рост звёзд/сутки — идёт в ранг
FRESH_DAYS = 4           # ГЛАВНЫЙ критерий: только игры за последние N дней (ежедневная порция)
TOY_STARS = 3            # 0★ без demo отсекаем как недоделку; с demo — берём даже 0★

# НОВЫЙ ПРИНЦИП (2026-09-10): только эти 5 свежайших моделей, окно 4 дня, ежедневно.
AI_TOOLS = [
    '"fable 5.1"', "fable", '"claude fable"',
    "astra", '"gpt-6-astra"',
    '"gpt-6"', "gpt6", '"gpt 6"',
    '"grok 4.6"', '"grok 4"',
    '"gemini 3.8"', '"gemini 3.8 flash"', '"gemini 3"',
]
GAME_TERMS = ["game", "game browser", "html5 game"]
# матрица: каждый AI-ключ × игровой термин  (~43×3 ≈ 130 запросов)
QUERIES = [f"{t} {g}" for t in AI_TOOLS for g in GAME_TERMS]
# + покрытие по движкам/vibe-топикам (свежие веб-игры вообще)
QUERIES += [
    "topic:vibe-coding game", '"vibe game"', "topic:threejs game",
    "topic:webgl game", "topic:html5-game", "topic:browser-game",
    "topic:phaser game", "topic:babylonjs game", "topic:webgpu game",
    "topic:aframe game",
]
# + «залипательная физика»: ragdoll / гравитация / стикмены / разрушение / песочницы.
# Смысл — сама механика физики залипательная, а не AI-модель. Ищем и по движкам физики.
PHYSICS_TERMS = [
    # ядро жанра
    '"physics game"', '"physics sandbox"', '"ragdoll physics"', "ragdoll game",
    '"gravity game"', '"gravity mod"', '"zero gravity" game',
    # стикмены / тряпичная кукла / расчленёнка / падения
    "stickman physics", '"stick fight"', '"ragdoll runner"',
    '"fall flat"', '"human fall"', '"getting over it"',
    "dismember physics", '"soft body" game', '"cloth simulation" game',
    # бросание / разрушение / складывание предметов
    '"destruction physics"', '"throw physics"', '"physics puzzle"',
    '"stacking" physics game', '"vehicle physics" game', '"car physics" game',
    "climbing physics game",
    # физ-движки (на них и делают такие игрушки)
    "matter.js game", "matter-js game", "box2d game", "planck.js game",
    "cannon.js game", "cannon-es game", "rapier physics game", "ammo.js game",
    # топики
    "topic:physics game", "topic:matter-js", "topic:ragdoll",
    "topic:physics-simulation game", "topic:box2d", "topic:2d-physics game",
]
QUERIES += PHYSICS_TERMS
PHYSICS_SET = set(PHYSICS_TERMS)   # по этим ключам действует длинный горизонт дат

PERMISSIVE = {"MIT", "APACHE-2.0", "BSD-2-CLAUSE", "BSD-3-CLAUSE", "ISC",
              "UNLICENSE", "CC0-1.0", "0BSD", "ZLIB", "MPL-2.0"}
COPYLEFT = {"GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-3.0", "LGPL-2.1"}
SERVER_DEPS = {"socket.io", "ws", "express", "fastify", "koa", "colyseus",
               "@colyseus/core", "uwebsockets.js", "hapi", "nakama-js"}
SERVER_FILES = {"server.js", "server.ts", "server.py", "app.py", "main.py",
                "go.mod", "cargo.toml", "gemfile", "composer.json", "manage.py",
                "docker-compose.yml", "docker-compose.yaml", "procfile"}
CLIENT_ENGINES = {"three", "@react-three/fiber", "phaser", "pixi.js", "babylonjs",
                  "@babylonjs/core", "aframe", "playcanvas", "kaboom", "kaplay", "excalibur"}
GENRE_GOOD = ["runner", "arcade", "racing", "kart", "tower defense", "tower-defense",
              "hyper-casual", "hypercasual", "casual", "puzzle", "clicker", "idle",
              "endless", "flappy", "crossy", "match-3", "shooter", ".io", "platformer"]
GENRE_HARD = ["rpg", "mmo", "simulator", "sandbox", "open world", "open-world",
              "strategy", "roguelike", "metroidvania"]
# признаки «не игра» (awesome-списки, инструменты, движки, шаблоны, туториалы)
JUNK_HINTS = ["awesome-", "awesome ", "list of", "curated", "collection of",
              "boilerplate", "starter template", "starter kit", "cheatsheet",
              "roadmap", "tutorial", "course", "handbook",
              "prompt collection", "prompts for", "prompt library", "awesome-prompts",
              "game engine", "engine for", "framework for", "sdk for",
              "plugin for", "template for", "asset pack",
              "design-tool", "design tool", "editor for", "component library",
              "cli tool", "vscode extension",
              "debug", "checker", "benchmark", "mentor", "devtool", "dev tool",
              "mcp server", "mcp-server", "task manager", "agent-deck", "agent deck",
              "fleet", "wrapper for", "for claude", "leaderboard service", "analytics"]

DEMO_RE = re.compile(r"(vercel\.app|netlify\.app|github\.io|itch\.io|pages\.dev|"
                     r"fly\.dev|onrender\.com|surge\.sh|glitch\.me)")
BADGE_RE = re.compile(r"(img\.shields\.io|badgen\.net|badge\.fury\.io|"
                      r"forthebadge|visitor-badge|hits\.)")


# ---------------------------------------------------------------- env / http

def h(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


_LOCK_FH = None
def acquire_lock():
    """Один инстанс краулера за раз — иначе гонка select→post даёт дубли постов."""
    global _LOCK_FH
    _LOCK_FH = open(os.path.join(HOME, ".crawler.lock"), "w")
    try:
        fcntl.flock(_LOCK_FH, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except OSError:
        return False


def load_env(path):
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def gh(path, token, params=None):
    """Возвращает (json|None, headers)."""
    h = {"Accept": "application/vnd.github+json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    for attempt in range(4):
        try:
            r = requests.get(f"{API}{path}", headers=h, params=params, timeout=30)
        except requests.RequestException as e:
            print(f"    net err: {e}", file=sys.stderr)
            time.sleep(3)
            continue
        if r.status_code == 200:
            return r.json(), r.headers
        if r.status_code == 404:
            return None, r.headers
        if r.status_code in (403, 429):
            reset = int(r.headers.get("x-ratelimit-reset", 0))
            wait = max(3, min(60, reset - int(time.time()) + 2)) if reset else 10 * (attempt + 1)
            print(f"    rate limit ({r.status_code}), sleep {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        print(f"    HTTP {r.status_code} {path}", file=sys.stderr)
        return None, r.headers
    return None, {}


def remaining(headers, default=9999):
    try:
        return int(headers.get("x-ratelimit-remaining", default))
    except (TypeError, ValueError):
        return default


def fetch_text(path, token):
    d, _ = gh(path, token)
    if not d or "content" not in d:
        return ""
    try:
        return base64.b64decode(d["content"]).decode("utf-8", "ignore")
    except Exception:
        return ""


# ---------------------------------------------------------------- db

def db():
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA busy_timeout=15000")
    con.execute("PRAGMA journal_mode=WAL")
    try:
        con.execute("ALTER TABLE repos ADD COLUMN src_query TEXT")
    except sqlite3.OperationalError:
        pass   # колонка уже есть
    con.executescript("""
    CREATE TABLE IF NOT EXISTS repos (
        full_name TEXT PRIMARY KEY,
        html_url TEXT, created_at TEXT, pushed_at TEXT,
        description TEXT, homepage TEXT, language TEXT, topics TEXT,
        size_kb INTEGER, is_fork INTEGER, archived INTEGER,
        license TEXT, backend INTEGER, engine TEXT,
        static_ok INTEGER, self_contained INTEGER, mobile INTEGER,
        genre_good INTEGER, yandex_ready INTEGER,
        fitness INTEGER, verdict TEXT, demo TEXT, media TEXT,
        stars INTEGER, forks INTEGER,
        first_seen INTEGER, last_seen INTEGER,
        enriched INTEGER DEFAULT 0, scored INTEGER DEFAULT 0,
        notified INTEGER DEFAULT 0, enrich_err INTEGER DEFAULT 0);

    CREATE TABLE IF NOT EXISTS star_history (
        full_name TEXT, ts INTEGER, stars INTEGER, forks INTEGER,
        PRIMARY KEY (full_name, ts));

    CREATE TABLE IF NOT EXISTS shards (
        base_query TEXT, win_start TEXT, win_end TEXT,
        status TEXT DEFAULT 'pending', next_page INTEGER DEFAULT 1,
        total_found INTEGER DEFAULT 0, updated_ts INTEGER DEFAULT 0,
        PRIMARY KEY (base_query, win_start));

    CREATE INDEX IF NOT EXISTS idx_repos_enriched ON repos(enriched);
    CREATE INDEX IF NOT EXISTS idx_repos_scored ON repos(scored, notified, fitness);
    CREATE INDEX IF NOT EXISTS idx_shards_status ON shards(status);
    """)
    con.commit()
    return con


RESCAN_HOURS = 6         # как часто пере-сканировать ключ (ловим свежесозданные репы)


def ensure_shards(con):
    """Модель '1 ключ = 1 свежий срез' (created:>=cutoff). Пере-скан каждые RESCAN_HOURS."""
    con.execute("DELETE FROM shards WHERE win_start!='recent'")   # чистим legacy недельные шарды
    now_ts = int(time.time())
    added = 0
    for q in QUERIES:
        cur = con.execute("SELECT status, updated_ts FROM shards "
                          "WHERE base_query=? AND win_start='recent'", (q,)).fetchone()
        if cur is None:
            con.execute("INSERT INTO shards(base_query,win_start,win_end) VALUES(?, 'recent','')", (q,))
            added += 1
        elif cur["status"] == "done" and now_ts - cur["updated_ts"] > RESCAN_HOURS * 3600:
            con.execute("UPDATE shards SET status='pending', next_page=1 "
                        "WHERE base_query=? AND win_start='recent'", (q,))
    con.commit()
    if added:
        print(f"  shards +{added} (ключей всего {len(QUERIES)})", file=sys.stderr)


# ---------------------------------------------------------------- discovery

def upsert_repo(con, r, now_ts, src_query=None):
    con.execute("""INSERT INTO repos
        (full_name, html_url, created_at, pushed_at, description, homepage,
         language, topics, size_kb, is_fork, archived, license, stars, forks,
         first_seen, last_seen, src_query)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(full_name) DO UPDATE SET
         pushed_at=excluded.pushed_at, description=excluded.description,
         homepage=excluded.homepage, language=excluded.language,
         topics=excluded.topics, size_kb=excluded.size_kb, license=excluded.license,
         stars=excluded.stars, forks=excluded.forks, last_seen=excluded.last_seen""",
        (r["full_name"], r["html_url"], r.get("created_at"), r.get("pushed_at"),
         r.get("description"), r.get("homepage"), r.get("language"),
         json.dumps(r.get("topics") or [], ensure_ascii=False), r.get("size"),
         1 if r.get("fork") else 0, 1 if r.get("archived") else 0,
         ((r.get("license") or {}).get("spdx_id") or "NOASSERTION"),
         r.get("stargazers_count"), r.get("forks_count"), now_ts, now_ts, src_query))
    con.execute("INSERT OR REPLACE INTO star_history VALUES (?,?,?,?)",
                (r["full_name"], now_ts, r.get("stargazers_count", 0), r.get("forks_count", 0)))


def discover(con, token):
    now_ts = int(time.time())
    calls = 0
    shards = con.execute(
        "SELECT * FROM shards WHERE status='pending' ORDER BY win_start DESC").fetchall()
    if not shards:
        print("  discovery: все шарды пройдены (до следующего рескана свежих недель)", file=sys.stderr)
        return
    for sh in shards:
        if calls >= SEARCH_CALLS_PER_RUN:
            break
        horizon = PHYSICS_CUTOFF_DAYS if sh["base_query"] in PHYSICS_SET else CUTOFF_DAYS
        cutoff = (datetime.now(timezone.utc)
                  - timedelta(days=horizon)).date().isoformat()
        q = f'{sh["base_query"]} created:>={cutoff} is:public'
        page = sh["next_page"]
        found = sh["total_found"]
        done = False
        while page <= MAX_PAGES and calls < SEARCH_CALLS_PER_RUN:
            data, hdr = gh("/search/repositories", token, params={
                "q": q, "sort": "updated", "order": "desc",
                "per_page": PER_PAGE, "page": page})
            calls += 1
            if remaining(hdr, 9999) < SEARCH_FLOOR:
                con.execute("UPDATE shards SET next_page=?, total_found=?, updated_ts=? "
                            "WHERE base_query=? AND win_start=?",
                            (page, found, now_ts, sh["base_query"], sh["win_start"]))
                con.commit()
                print(f"  discovery: search floor, стоп ({calls} calls)", file=sys.stderr)
                return
            items = (data or {}).get("items", [])
            for r in items:
                upsert_repo(con, r, now_ts, sh["base_query"])
                found += 1
            con.commit()
            time.sleep(SEARCH_PACE)
            if len(items) < PER_PAGE:
                done = True
                break
            page += 1
        else:
            done = page > MAX_PAGES
        status = "done" if done else "pending"
        con.execute("UPDATE shards SET status=?, next_page=?, total_found=?, updated_ts=? "
                    "WHERE base_query=? AND win_start=?",
                    (status, 1 if done else page, found, now_ts, sh["base_query"], sh["win_start"]))
        con.commit()
    print(f"  discovery: {calls} search-запросов", file=sys.stderr)


# ---------------------------------------------------------------- enrich + score

def score_repo(meta, langs, root_files, deps, blob, demo, has_static_demo):
    dep_names = {d.lower() for d in deps}
    lic = ((meta.get("license") or {}).get("spdx_id") or "NOASSERTION").upper()

    server_hits = ([f for f in SERVER_FILES if f in root_files] +
                   [d for d in SERVER_DEPS if d in dep_names] +
                   [l for l in langs if l in ("Python", "Go", "Rust", "PHP", "Ruby", "Java", "C#")])
    backend = bool(server_hits)

    engine = next((e for e in CLIENT_ENGINES if e in dep_names), None)
    if not engine:
        for e in ("three", "phaser", "babylon", "pixi", "aframe", "webgl", "webgpu"):
            if e in blob:
                engine = e
                break

    has_index = "index.html" in root_files
    has_vite = ("vite.config.js" in root_files or "vite.config.ts" in root_files
                or "vite" in dep_names)
    static_ok = has_index or has_vite or has_static_demo

    self_contained = any(k in blob for k in
                         ["procedural", "no external", "no third-party", "no assets",
                          "generated at runtime", "single html", "one html file",
                          "no build step", "no cdn", "процедурн"])
    mobile = any(k in blob for k in
                 ["touch", "mobile", "responsive", "portrait", "мобил", "тач"])
    yandex_ready = "yandex" in blob or "яндекс" in blob
    genre_good = any(g in blob for g in GENRE_GOOD)
    genre_hard = any(g in blob for g in GENRE_HARD)
    size_kb = meta.get("size", 0) or 0

    name_desc = (meta.get("full_name", "") + " " + (meta.get("description") or "") + " "
                 + " ".join(meta.get("topics") or [])).lower()
    junk = any(k in name_desc for k in JUNK_HINTS) or bool(meta.get("archived"))

    score = 0
    if lic in PERMISSIVE:
        score += 25
    elif lic in COPYLEFT:
        score += 12
    # NOASSERTION / прочее — 0 (флаг лицензии смотрим на публикации)
    if static_ok:
        score += 20
    if self_contained:
        score += 15
    if mobile:
        score += 12
    if genre_good:
        score += 8
    if genre_hard:
        score -= 5
    if demo:
        score += 8
    if 0 < size_kb < 20000:
        score += 5
    elif size_kb >= 100000:
        score -= 5
    if yandex_ready:
        score += 5
    # backend больше НЕ штраф (io/сервер допустимы) — только тег
    score = max(0, min(100, score))
    if junk:
        score = min(score, 25)   # не-игра/инструмент → вниз, в дайджест не попадёт
    verdict = "junk" if junk else ("green" if score >= 65 else ("yellow" if score >= 40 else "red"))

    return dict(license=lic, backend=int(backend), engine=engine,
                static_ok=int(static_ok), self_contained=int(self_contained),
                mobile=int(mobile), genre_good=int(genre_good),
                yandex_ready=int(yandex_ready), fitness=score, verdict=verdict)


def extract_media(readme, full_name):
    media = []
    media += re.findall(r'!\[[^\]]*\]\(([^)\s]+)', readme)
    media += re.findall(r'<img[^>]+src=["\']([^"\']+)', readme)
    media += re.findall(r'<video[^>]+src=["\']([^"\']+)', readme)
    media += re.findall(r'<source[^>]+src=["\']([^"\']+)', readme)
    for m in re.findall(r'https?://[^\s)\]"\'<>]+', readme):
        if re.search(r'\.(gif|mp4|webm|png|jpg|jpeg|webp)(\?|$)|youtu\.be|'
                     r'youtube\.com/watch|itch\.io|vimeo', m, re.I):
            media.append(m)
    out, seen = [], set()
    for u in media:
        if BADGE_RE.search(u):
            continue
        if u.startswith("http"):
            full = u
        elif u.startswith("/"):
            full = f"https://github.com/{full_name}/raw/HEAD{u}"
        else:
            full = f"https://github.com/{full_name}/raw/HEAD/{u.lstrip('./')}"
        if full not in seen:
            seen.add(full)
            out.append(full)
    return out[:6]


def enrich(con, token):
    # пре-фильтр: не тратим core-бюджет на явно-не-игры (по данным поиска)
    rows = con.execute(
        "SELECT full_name FROM repos WHERE enriched=0 AND is_fork=0 "
        "AND (lower(full_name) LIKE '%game%' OR lower(coalesce(description,'')) LIKE '%game%' "
        "     OR lower(coalesce(topics,'')) LIKE '%game%' "
        "     OR lower(coalesce(topics,'')) LIKE '%playable%') "
        "ORDER BY created_at DESC LIMIT ?", (ENRICH_REPOS_PER_RUN,)).fetchall()
    if not rows:
        print("  enrich: очередь пуста", file=sys.stderr)
        return
    done = 0
    for row in rows:
        fn = row["full_name"]
        meta, hdr = gh(f"/repos/{fn}", token)
        if remaining(hdr, 9999) < CORE_FLOOR:
            print(f"  enrich: core floor, стоп ({done} готово)", file=sys.stderr)
            break
        if meta is None:
            con.execute("UPDATE repos SET enrich_err=enrich_err+1, enriched=? "
                        "WHERE full_name=?", (0, fn))
            con.commit()
            continue
        langs, _ = gh(f"/repos/{fn}/languages", token)
        contents, _ = gh(f"/repos/{fn}/contents", token)
        langs = langs or {}
        root_files = {c["name"].lower(): c for c in contents} if isinstance(contents, list) else {}

        deps = {}
        if "package.json" in root_files:
            try:
                deps = json.loads(fetch_text(f"/repos/{fn}/contents/package.json", token) or "{}")
                deps = {**deps.get("dependencies", {}), **deps.get("devDependencies", {})}
            except Exception:
                deps = {}

        readme = fetch_text(f"/repos/{fn}/readme", token)
        desc = (meta.get("description") or "")
        topics = " ".join(meta.get("topics") or [])
        blob = " ".join([desc, topics, readme[:5000]]).lower()

        homepage = meta.get("homepage") or ""
        has_static_demo = bool(homepage) and bool(DEMO_RE.search(homepage))
        demo = homepage if (has_static_demo or homepage) else ""
        media = extract_media(readme, fn)

        sc = score_repo(meta, langs, root_files, deps, blob, demo, has_static_demo)

        con.execute("""UPDATE repos SET
            license=?, backend=?, engine=?, static_ok=?, self_contained=?, mobile=?,
            genre_good=?, yandex_ready=?, fitness=?, verdict=?, demo=?, media=?,
            size_kb=?, enriched=1, scored=1 WHERE full_name=?""",
            (sc["license"], sc["backend"], sc["engine"], sc["static_ok"],
             sc["self_contained"], sc["mobile"], sc["genre_good"], sc["yandex_ready"],
             sc["fitness"], sc["verdict"], demo,
             json.dumps(media, ensure_ascii=False), meta.get("size", 0), fn))
        con.commit()
        done += 1
        time.sleep(CORE_PACE)
    print(f"  enrich: {done} реп обогащено", file=sys.stderr)


# ---------------------------------------------------------------- digest

def tg_token():
    load_env(TG_ENV_PATH)
    return os.environ.get("TELEGRAM_BOT_TOKEN")


def tg_api(method, tok, data=None, files=None):
    try:
        r = requests.post(f"https://api.telegram.org/bot{tok}/{method}",
                          timeout=120, data=data, files=files)
        if r.status_code != 200:
            print(f"  tg {method}: {r.status_code} {r.text[:200]}", file=sys.stderr)
        return r.status_code == 200
    except requests.RequestException as e:
        print(f"  tg {method}: {e}", file=sys.stderr)
        return False


def tg_send_text(tok, text):
    return tg_api("sendMessage", tok, data={
        "chat_id": TG_CHAT_ID, "text": text, "parse_mode": "HTML",
        "disable_web_page_preview": "true"})


def normalize_image(path):
    """Пере-кодируем в безопасный для Telegram JPEG (иначе бывает IMAGE_PROCESS_FAILED).
    Возвращает путь к .jpg или None, если это не картинка."""
    try:
        from PIL import Image
        im = Image.open(path)
        im = im.convert("RGB")
        im.thumbnail((1600, 1600))
        out = path.rsplit(".", 1)[0] + "_n.jpg"
        im.save(out, "JPEG", quality=85)
        return out if os.path.getsize(out) > 1500 else None
    except Exception as e:
        print(f"  img skip ({os.path.basename(path)}): {e}", file=sys.stderr)
        return None


def send_photos(tok, photos, cap):
    """Шлём фото альбомом; если альбом упал (битая картинка) — по одному, битые пропускаем."""
    photos = photos[:10]
    if len(photos) >= 2:
        media, files = [], {}
        for i, p in enumerate(photos):
            files[f"p{i}"] = open(p, "rb")
            it = {"type": "photo", "media": f"attach://p{i}"}
            if i == 0:
                it["caption"] = cap[:1024]; it["parse_mode"] = "HTML"
            media.append(it)
        okg = tg_api("sendMediaGroup", tok,
                     data={"chat_id": TG_CHAT_ID, "media": json.dumps(media)}, files=files)
        for f in files.values():
            f.close()
        if okg:
            return True
        print("  media group упал → шлю по одному", file=sys.stderr)
    ok_any = False
    for i, p in enumerate(photos):
        with open(p, "rb") as f:
            d = {"chat_id": TG_CHAT_ID}
            if i == 0:
                d["caption"] = cap[:1024]; d["parse_mode"] = "HTML"
            if tg_api("sendPhoto", tok, data=d, files={"photo": f}):
                ok_any = True
    return ok_any


def shoot_demo(url, dest):
    """Скриншот живого demo через headless Chrome. True при успехе."""
    if not url:
        return False
    profile = os.path.join(SHOTS_DIR, ".prof-" + str(int(time.time() * 1000)))
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
           "--disable-dev-shm-usage", "--mute-audio", "--hide-scrollbars",
           "--no-first-run", "--window-size=1280,720",
           "--use-gl=angle", "--use-angle=swiftshader-webgl", "--enable-webgl",
           "--force-device-scale-factor=1", f"--user-data-dir={profile}",
           "--virtual-time-budget=6000", f"--screenshot={dest}", url]
    try:
        import subprocess
        subprocess.run(cmd, timeout=32, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"  shoot: {e}", file=sys.stderr)
    finally:
        try:
            import shutil
            shutil.rmtree(profile, ignore_errors=True)
        except Exception:
            pass
    return os.path.exists(dest) and os.path.getsize(dest) > 3000


def fetch_file(url, dest_base):
    """Качает медиа. Возвращает (path, kind) kind in photo/animation/video, или None."""
    try:
        r = requests.get(url, timeout=40, stream=True,
                         headers={"User-Agent": "vibegame-radar"})
        if r.status_code != 200:
            return None
        ct = r.headers.get("content-type", "").lower()
        if "image/gif" in ct:
            kind, ext = "animation", ".gif"
        elif ct.startswith("image/"):
            kind, ext = "photo", ".png"
        elif "video/mp4" in ct or "video/webm" in ct:
            kind, ext = "video", ".mp4"
        else:
            return None
        path = dest_base + ext
        size = 0
        with open(path, "wb") as f:
            for chunk in r.iter_content(65536):
                size += len(chunk)
                if size > 18 * 1024 * 1024:      # cap 18MB
                    f.close(); os.remove(path); return None
                f.write(chunk)
        if size < 2000:
            os.remove(path); return None
        return path, kind
    except requests.RequestException:
        return None


def conclude(r):
    """Короткий практический ВЫВОД по игре: что делать для порта на Яндекс."""
    lic = (r["license"] or "").upper()
    if lic in ("NOASSERTION", "NONE", ""):
        base = "нет лицензии — форк под вопросом, писать автору"
    elif r["backend"]:
        base = "нужен хостинг бэкенда (io/сервер) — иначе резать до статики"
    elif r["static_ok"] and r["mobile"]:
        base = "готов к порту: статика + тач, добавить только Yandex SDK"
    elif r["static_ok"]:
        base = "порт лёгкий: статика есть, доделать тач + Yandex SDK"
    else:
        base = "проверить сборку статики, добавить тач + Yandex SDK"
    if not r["demo"]:
        base += " · demo нет (репа «для себя») — собрать/задеплоить и глянуть"
    return base


def caption_for(r, vel=0.0):
    dot = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(r["verdict"], "")
    age = ""
    try:
        c = datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
        age = f' · {int((datetime.now(timezone.utc) - c).days)}д'
    except Exception:
        pass
    tags = []
    if r["engine"]:
        tags.append(r["engine"])
    tags.append(r["license"])
    if r["backend"]:
        tags.append("есть сервер")
    if r["static_ok"]:
        tags.append("статика")
    if r["mobile"]:
        tags.append("тач")
    if r["self_contained"]:
        tags.append("self-contained")
    desc = (r["description"] or "").strip()
    if len(desc) > 320:
        desc = desc[:317] + "…"
    vel_s = f' · 📈{vel}/сут' if vel and vel >= 1 else ''
    ai_s = '🤖 AI · ' if ai_signal(r) else ''
    age_s = age.replace(' · ', '🆕 ') if age else ''
    lines = [f'{dot} {ai_s}<b>{h(r["full_name"])}</b>',
             f'{age_s} · ⭐{r["stars"]}{vel_s} · fitness {r["fitness"]} · {" · ".join(t for t in tags if t)}']
    if desc:
        lines.append(desc)
    lines.append(f'📦 репо: {r["html_url"]}')
    if r["demo"]:
        lines.append(f'▶️ demo: {r["demo"]}')
    lines.append(f'📝 вывод: {conclude(r)}')
    return "\n".join(lines)


def post_game(tok, r, vel=0.0):
    """1 игра = 1 пост: скрин demo + медиа из README, файлами, с подписью."""
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", r["full_name"])
    photos, gifs, videos = [], [], []

    # 1) живой скрин demo (герой)
    if r["demo"]:
        shot = os.path.join(SHOTS_DIR, f"{slug}_demo.png")
        if shoot_demo(r["demo"], shot):
            photos.append(shot)

    # 2) медиа из README
    for i, url in enumerate(json.loads(r["media"] or "[]")):
        if len(photos) >= 6 and gifs and videos:
            break
        got = fetch_file(url, os.path.join(SHOTS_DIR, f"{slug}_m{i}"))
        if not got:
            continue
        path, kind = got
        if kind == "photo" and len(photos) < 6:
            photos.append(path)
        elif kind == "animation" and len(gifs) < 2:
            gifs.append(path)
        elif kind == "video" and len(videos) < 1:
            videos.append(path)

    # нормализуем все фото в безопасный JPEG (чинит IMAGE_PROCESS_FAILED), битые выкидываем
    photos = [n for n in (normalize_image(p) for p in photos) if n]

    # постим, если есть визуал; если визуала нет — только когда есть demo/сборка/звёзды
    if (not photos and not gifs and not videos
            and not r["demo"] and not r["static_ok"] and (r["stars"] or 0) < TOY_STARS):
        return False

    cap = caption_for(r, vel)
    if photos:
        ok = send_photos(tok, photos, cap)
    else:
        ok = tg_send_text(tok, cap)

    # гифки и видео — отдельными сообщениями
    for g in gifs:
        with open(g, "rb") as f:
            tg_api("sendAnimation", tok, data={"chat_id": TG_CHAT_ID}, files={"animation": f})
    for v in videos:
        with open(v, "rb") as f:
            tg_api("sendVideo", tok, data={"chat_id": TG_CHAT_ID}, files={"video": f})
    return ok


def velocity(con, fn):
    """Рост звёзд/сутки по star_history (0, если истории мало)."""
    rows = con.execute("SELECT ts, stars FROM star_history WHERE full_name=? "
                       "ORDER BY ts", (fn,)).fetchall()
    if len(rows) < 2:
        return 0.0
    t0, s0 = rows[0]["ts"], rows[0]["stars"]
    t1, s1 = rows[-1]["ts"], rows[-1]["stars"]
    days = max((t1 - t0) / 86400, 0.25)
    return round((s1 - s0) / days, 1)


# сильные игровые топики (сам факт = игра); generic "game"/"gamedev" тут НЕ считаем — их юзают и либы
STRONG_GAME_TOPICS = {"html5-game", "browser-game", "webgame", "web-game", "indie-game",
                      "indiegame", "2d-game", "3d-game", "multiplayer-game", "io-game",
                      "idle-game", "incremental-game", "roguelike", "platformer",
                      "tower-defense", "arcade-game", "puzzle-game", "racing-game",
                      "shooter-game", "gamejam", "game-jam", "html5-canvas-game"}
# веб-сигнал: игра реально в браузере
WEB_TOPICS = {"html5-game", "browser-game", "webgame", "web-game", "threejs", "three-js",
              "webgl", "webgpu", "phaser", "babylonjs", "pixijs", "html5", "html5-canvas",
              "javascript-game", "webassembly", "wasm", "react-three-fiber", "aframe"}
WEB_LANGS = {"JavaScript", "TypeScript", "HTML", "Svelte", "Vue", "Astro"}
# тул/не-игра сигналы (по топикам и тексту)
TOOL_TOPICS = {"gdextension", "godot-addon", "extension", "addon", "plugin", "library",
               "framework", "sdk", "data-analytics", "analytics", "data-science",
               "game-hacking", "cheat", "cheat-engine", "reverse-engineering", "mod",
               "modding", "dotfiles", "cli", "devtools", "boilerplate", "template",
               "starter-kit", "toolkit", "dataset", "benchmark", "api-wrapper",
               "dos", "dosbox", "dosgame", "dos-game", "emulator", "emulation", "rom"}
TOOL_WORDS = ["terminal", " ide ", "code editor", "compiler", "runtime", "filesystem",
              "file system", " vfs", "framework", "library", "addon", "add-on",
              "plugin", "profiles", "dashboard", " cli ", " sdk", "benchmark",
              "boilerplate", "wrapper", "dotfiles", "toolkit", "devtool", "cheat",
              "hacking", "analytics", "extension for", "scaffold", "orchestrat",
              "linter", "formatter", "dataset", "reverse engineer"]
GAME_WORD_RE = re.compile(r'\bgame\b|\bгейм|\bигр|\bplayable\b|\bgameplay\b')


def is_game(r):
    """Гейт «это реально ВЕБ-игра» по сохранённым topics+описанию+языку (без пере-обогащения)."""
    try:
        topics = set(json.loads(r["topics"] or "[]"))
    except Exception:
        topics = set()
    text = f'{r["full_name"]} {r["description"] or ""}'.lower()
    lang = r["language"] or ""

    # тул/не-игра → сразу мимо
    if topics & TOOL_TOPICS:
        return False
    if any(w in text for w in TOOL_WORDS):
        return False

    # это вообще игра?
    game_signal = bool(topics & STRONG_GAME_TOPICS) or bool(GAME_WORD_RE.search(text))
    if not game_signal:
        return False

    # это ВЕБ-игра? (иначе нативное C/DOS/десктоп — не под Яндекс)
    web_signal = (bool(r["demo"]) or bool(topics & WEB_TOPICS)
                  or lang in WEB_LANGS or bool(r["static_ok"]))
    return web_signal


AI_HINTS = ["claude", "gpt", "cursor", "codex", "copilot", "vibe", "v0.dev",
            "v0 ", "bolt.new", "bolt ", "lovable", "windsurf", "replit agent",
            "ai-generated", "ai generated", "ai-built", "llm", "anthropic", "openai",
            "промпт", "нейросет",
            # топ-модели
            "qwen", "astra", "fable", "grok", "gemini", "deepseek", "kimi",
            "glm", "minimax", "opus", "sonnet"]


def ai_signal(r):
    text = f'{r["full_name"]} {r["description"] or ""} {r["topics"] or ""}'.lower()
    return any(k in text for k in AI_HINTS)


def days_since(iso):
    try:
        d = datetime.fromisoformat((iso or "").replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - d).days
    except Exception:
        return 9999


def select_candidates(con, cap):
    """Критерии отбора: СВЕЖЕСТЬ (created) + это веб-игра + AI-ключ. Без звёзд и fitness-гейта.
    Клоны допускаются. Ранг: свежесть (главное) + AI + рабочий demo."""
    cand = con.execute(
        "SELECT * FROM repos WHERE scored=1 AND notified=0 AND verdict!='junk'"
    ).fetchall()
    out = []
    for r in cand:
        if not is_game(r):                 # оставляем только настоящие веб-игры
            continue
        age = days_since(r["created_at"])
        is_phys = (r["src_query"] or "") in PHYSICS_SET
        horizon = PHYSICS_CUTOFF_DAYS if is_phys else FRESH_DAYS
        if age > horizon:                  # свежесть: AI-ключи 4 дня, физ-ключи ~90 дней
            continue
        # 0★ берём, если есть хоть какой сигнал пригодности: demo ИЛИ скрины/медиа
        # ИЛИ быстро собирается (статика/сборка). Люди часто пушат «для себя» без витрины.
        try:
            has_media = bool(json.loads(r["media"] or "[]"))
        except Exception:
            has_media = False
        usable = (bool(r["demo"]) or has_media or bool(r["static_ok"])
                  or (r["stars"] or 0) >= TOY_STARS)
        if not usable:
            continue
        ai = ai_signal(r)
        vel = velocity(con, r["full_name"])
        # ранг: чем свежее — тем выше; AI-игры и с demo — вперёд.
        # свежесть нормируем в единую полосу 0..40, чтобы физ-игры (горизонт 90д)
        # не забивали AI-свежак и наоборот — сравнение идёт «в своём окне».
        fresh_pts = max(0.0, (horizon - age) / horizon) * 40
        rank = (fresh_pts
                + (35 if ai else 0)
                + (20 if r["demo"] else 0)
                + min(vel, 30) * 1.5
                + r["fitness"] * 0.1)          # fitness — лишь лёгкий тай-брейк
        out.append((rank, vel, r))
    out.sort(key=lambda x: -x[0])
    return out[:cap]


def digest(con, force_empty=False, cap=DIGEST_MAX):
    cands = select_candidates(con, cap)
    rows = [(r, vel) for _, vel, r in cands]
    tok = tg_token()
    if not tok:
        print("  digest: нет TELEGRAM_BOT_TOKEN", file=sys.stderr)
        return
    os.makedirs(SHOTS_DIR, exist_ok=True)
    # чистим скрины старше 2 суток
    cutoff = time.time() - 2 * 86400
    for fn in os.listdir(SHOTS_DIR):
        p = os.path.join(SHOTS_DIR, fn)
        try:
            if os.path.isfile(p) and os.path.getmtime(p) < cutoff:
                os.remove(p)
        except OSError:
            pass
    if not rows:
        print("  digest: новых находок нет", file=sys.stderr)
        if force_empty:
            tg_send_text(tok, "🎮 VibeGame Radar: за сутки новых подходящих игр не найдено.")
        return
    if cap >= DIGEST_MAX:     # шапку шлём только у ручного/дневного дайджеста, не в realtime
        tg_send_text(tok, f"🎮 <b>VibeGame Radar</b> — {len(rows)} новых кандидатов под Яндекс.Игры 👇")
    posted = 0
    for r, vel in rows:
        try:
            if post_game(tok, r, vel):
                con.execute("UPDATE repos SET notified=1 WHERE full_name=?", (r["full_name"],))
                con.commit()
                posted += 1
            time.sleep(1.5)
        except Exception as e:
            print(f"  digest {r['full_name']}: {e}", file=sys.stderr)
    print(f"  digest: {posted}/{len(rows)} постов", file=sys.stderr)


# ---------------------------------------------------------------- status

def keys_report(con):
    rows = con.execute(
        "SELECT src_query, COUNT(*) total, "
        "SUM(CASE WHEN verdict IN ('green','yellow') THEN 1 ELSE 0 END) games, "
        "SUM(CASE WHEN notified=1 THEN 1 ELSE 0 END) posted "
        "FROM repos WHERE src_query IS NOT NULL GROUP BY src_query "
        "ORDER BY games DESC, total DESC").fetchall()
    if not rows:
        print("src_query ещё пуст — наполнится со следующего прочёса", file=sys.stderr)
        return
    print(f"{'games':>5} {'posted':>6} {'total':>6}  ключ")
    for r in rows[:45]:
        print(f"{r['games'] or 0:>5} {r['posted'] or 0:>6} {r['total']:>6}  {r['src_query']}")


def status(con):
    g = con.execute("SELECT COUNT(*) FROM repos").fetchone()[0]
    en = con.execute("SELECT COUNT(*) FROM repos WHERE enriched=1").fetchone()[0]
    q = con.execute("SELECT COUNT(*) FROM repos WHERE enriched=0 AND is_fork=0").fetchone()[0]
    sp = con.execute("SELECT COUNT(*) FROM shards WHERE status='pending'").fetchone()[0]
    sd = con.execute("SELECT COUNT(*) FROM shards WHERE status='done'").fetchone()[0]
    gr = con.execute("SELECT COUNT(*) FROM repos WHERE verdict='green'").fetchone()[0]
    ye = con.execute("SELECT COUNT(*) FROM repos WHERE verdict='yellow'").fetchone()[0]
    nt = con.execute("SELECT COUNT(*) FROM repos WHERE notified=1").fetchone()[0]
    print(f"repos={g}  enriched={en}  queue={q}  | shards done={sd} pending={sp}")
    print(f"verdict: green={gr} yellow={ye}  | notified={nt}")
    top = con.execute("SELECT full_name, fitness, stars, verdict FROM repos "
                      "WHERE scored=1 ORDER BY fitness DESC LIMIT 10").fetchall()
    for t in top:
        print(f"  {t['fitness']:>3} ⭐{t['stars']:<5} {t['verdict']:<6} {t['full_name']}")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="ensure-shards + discovery + enrich")
    ap.add_argument("--discover", action="store_true")
    ap.add_argument("--enrich", action="store_true")
    ap.add_argument("--digest", action="store_true")
    ap.add_argument("--digest-empty", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--keys", action="store_true")
    args = ap.parse_args()

    load_env(ENV_PATH)
    token = os.environ.get("GITHUB_TOKEN")
    con = db()

    if args.status:
        status(con); return
    if args.keys:
        keys_report(con); return

    # действия, которые пишут/постят — только одним инстансом (защита от дублей)
    if not acquire_lock():
        print("другой инстанс краулера уже работает — выходим (защита от дублей)", file=sys.stderr)
        return
    if args.digest or args.digest_empty:
        digest(con, force_empty=args.digest_empty); return

    if args.run or args.discover:
        ensure_shards(con)
        discover(con, token)
    if args.run or args.enrich:
        enrich(con, token)
    if args.run:
        digest(con, cap=REALTIME_MAX)   # realtime: постим новые находки сразу
    if not any([args.run, args.discover, args.enrich]):
        ap.print_help()


if __name__ == "__main__":
    main()
