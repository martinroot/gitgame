#!/usr/bin/env python3
"""
vibegame_radar.py — радар свежих хайповых vibe-coded игровых репозиториев на GitHub.

Логика:
  1. Гоняем набор поисковых запросов по GitHub Search API (свежие репы, N дней).
  2. Кладём снапшот в SQLite -> при следующем запуске считаем ДЕЛЬТУ звёзд
     (реальная скорость хайпа, а не абсолютные звёзды).
  3. Скорим: velocity + бонусы за playable demo, движок, свежесть.
  4. Отдаём топ в stdout / JSON / Telegram.

Запуск:
  export GITHUB_TOKEN=ghp_...        # без токена 10 запросов/мин, с токеном 30/мин
  python3 vibegame_radar.py --days 30 --top 20
  python3 vibegame_radar.py --days 14 --telegram      # нужны TG_BOT_TOKEN, TG_CHAT_ID
"""

import argparse
import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timedelta, timezone

import requests

API = "https://api.github.com"
DB_PATH = os.environ.get("VG_DB", os.path.join(os.path.dirname(os.path.abspath(__file__)), "radar.db"))

# Наборы запросов. Каждый — отдельный вызов search API, поэтому держим их осмысленными.
QUERY_TEMPLATES = [
    'topic:vibe-coding topic:game',
    'topic:vibecoding game',
    '"vibe coded" game',
    '"vibe game"',
    'topic:threejs topic:game',
    'topic:babylonjs game',
    'topic:webgl game multiplayer',
    'topic:game-development ai-generated',
    '"built with cursor" game',
    '"claude code" game browser',
]

ENGINE_HINTS = {
    "three.js": 3, "threejs": 3, "babylon": 3, "r3f": 3, "react-three-fiber": 3,
    "phaser": 2, "pixi": 2, "godot": 2, "webgpu": 3, "webgl": 2,
    "unity": 1, "bevy": 2, "noa": 3,
}
VIBE_HINTS = {
    "vibe": 4, "vibe-coded": 5, "vibecoding": 5, "cursor": 2, "claude": 2,
    "gpt": 1, "ai-generated": 3, "prompt": 1, "copilot": 1,
}
MONETIZATION_HINTS = {
    "multiplayer": 3, "mmo": 3, ".io": 2, "leaderboard": 2, "mobile": 2,
    "telegram": 3, "mini app": 3, "miniapp": 3, "tma": 2,
}

DEMO_RE = re.compile(r"(vercel\.app|netlify\.app|github\.io|itch\.io|pages\.dev|fly\.dev|onrender\.com)")


# ---------------------------------------------------------------- storage

def db_init():
    con = sqlite3.connect(DB_PATH)
    con.execute("""CREATE TABLE IF NOT EXISTS snapshots (
        full_name TEXT NOT NULL,
        ts        INTEGER NOT NULL,
        stars     INTEGER NOT NULL,
        forks     INTEGER NOT NULL,
        PRIMARY KEY (full_name, ts))""")
    con.execute("""CREATE TABLE IF NOT EXISTS seen (
        full_name TEXT PRIMARY KEY,
        first_ts  INTEGER NOT NULL,
        notified  INTEGER NOT NULL DEFAULT 0)""")
    con.commit()
    return con


def prev_snapshot(con, full_name, now_ts):
    row = con.execute(
        "SELECT ts, stars FROM snapshots WHERE full_name=? AND ts < ? ORDER BY ts DESC LIMIT 1",
        (full_name, now_ts - 3600),
    ).fetchone()
    return row  # (ts, stars) | None


def save_snapshot(con, repo, now_ts):
    con.execute("INSERT OR REPLACE INTO snapshots VALUES (?,?,?,?)",
                (repo["full_name"], now_ts, repo["stargazers_count"], repo["forks_count"]))
    con.execute("INSERT OR IGNORE INTO seen (full_name, first_ts) VALUES (?,?)",
                (repo["full_name"], now_ts))


# ---------------------------------------------------------------- github

def gh_search(query, since_date, per_page=50, token=None):
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    q = f"{query} created:>{since_date} is:public"
    for attempt in range(4):
        r = requests.get(f"{API}/search/repositories", headers=headers, timeout=30,
                         params={"q": q, "sort": "stars", "order": "desc", "per_page": per_page})
        if r.status_code == 200:
            return r.json().get("items", [])
        if r.status_code in (403, 429):
            reset = int(r.headers.get("x-ratelimit-reset", 0))
            wait = max(5, min(70, reset - int(time.time()) + 2)) if reset else 15 * (attempt + 1)
            print(f"  rate limit, sleep {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        print(f"  HTTP {r.status_code} на «{query}»", file=sys.stderr)
        return []
    return []


# ---------------------------------------------------------------- scoring

def keyword_score(text, table):
    text = (text or "").lower()
    return sum(w for k, w in table.items() if k in text)


def score_repo(repo, con, now_ts):
    created = datetime.fromisoformat(repo["created_at"].replace("Z", "+00:00"))
    pushed = datetime.fromisoformat(repo["pushed_at"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    age_days = max(0.5, (now - created).total_seconds() / 86400)
    stale_days = (now - pushed).total_seconds() / 86400

    stars = repo["stargazers_count"]
    blob = " ".join(filter(None, [
        repo.get("description"), repo.get("name"),
        " ".join(repo.get("topics") or []), repo.get("homepage"),
    ]))

    # Скорость: дельта между запусками, если она есть; иначе средняя за жизнь репы.
    prev = prev_snapshot(con, repo["full_name"], now_ts)
    if prev:
        prev_ts, prev_stars = prev
        hours = max(1.0, (now_ts - prev_ts) / 3600)
        velocity = (stars - prev_stars) / hours * 24  # звёзд/сутки
        vel_source = "delta"
    else:
        velocity = stars / age_days
        vel_source = "avg"

    has_demo = bool(repo.get("homepage")) and bool(DEMO_RE.search(repo.get("homepage") or ""))

    score = velocity * 10
    score += keyword_score(blob, VIBE_HINTS) * 4
    score += keyword_score(blob, ENGINE_HINTS) * 3
    score += keyword_score(blob, MONETIZATION_HINTS) * 3
    score += 25 if has_demo else 0
    score += 15 if stale_days < 3 else (5 if stale_days < 10 else 0)   # живой проект
    score -= 20 if repo.get("fork") else 0
    score -= 15 if stars < 5 else 0

    return {
        "full_name": repo["full_name"],
        "url": repo["html_url"],
        "desc": (repo.get("description") or "")[:180],
        "stars": stars,
        "forks": repo["forks_count"],
        "lang": repo.get("language"),
        "topics": (repo.get("topics") or [])[:6],
        "homepage": repo.get("homepage") or "",
        "has_demo": has_demo,
        "age_days": round(age_days, 1),
        "stale_days": round(stale_days, 1),
        "velocity": round(velocity, 1),
        "vel_source": vel_source,
        "score": round(score, 1),
    }


# ---------------------------------------------------------------- output

def to_telegram(items, limit=10):
    lines = ["🎮 <b>VibeGame Radar</b> — свежий хайп на GitHub\n"]
    for i, it in enumerate(items[:limit], 1):
        demo = f' · <a href="{it["homepage"]}">demo</a>' if it["has_demo"] else ""
        lines.append(
            f'{i}. <a href="{it["url"]}">{it["full_name"]}</a>{demo}\n'
            f'   ⭐ {it["stars"]} · {it["velocity"]}/сут · {it["age_days"]}д · {it["lang"] or "—"}\n'
            f'   <i>{it["desc"]}</i>\n'
        )
    return "\n".join(lines)


def send_telegram(text):
    tok, chat = os.environ.get("TG_BOT_TOKEN"), os.environ.get("TG_CHAT_ID")
    if not (tok and chat):
        print("TG_BOT_TOKEN / TG_CHAT_ID не заданы", file=sys.stderr)
        return
    r = requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", timeout=30, json={
        "chat_id": chat, "text": text, "parse_mode": "HTML",
        "disable_web_page_preview": True})
    print("telegram:", r.status_code, file=sys.stderr)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30, help="окно свежести репозиториев")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--min-stars", type=int, default=3)
    ap.add_argument("--json", metavar="PATH")
    ap.add_argument("--telegram", action="store_true")
    ap.add_argument("--only-new", action="store_true", help="только те, что ещё не отправлялись")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    since = (datetime.now(timezone.utc) - timedelta(days=args.days)).strftime("%Y-%m-%d")
    now_ts = int(time.time())
    con = db_init()

    raw = {}
    for q in QUERY_TEMPLATES:
        print(f"[q] {q}", file=sys.stderr)
        for repo in gh_search(q, since, token=token):
            raw[repo["full_name"]] = repo
        time.sleep(2 if token else 7)   # держимся в лимите search API

    scored = []
    for repo in raw.values():
        if repo["stargazers_count"] < args.min_stars:
            continue
        scored.append(score_repo(repo, con, now_ts))
        save_snapshot(con, repo, now_ts)
    con.commit()

    if args.only_new:
        fresh = {r[0] for r in con.execute("SELECT full_name FROM seen WHERE notified=0")}
        scored = [s for s in scored if s["full_name"] in fresh]

    scored.sort(key=lambda x: -x["score"])
    top = scored[: args.top]

    for i, it in enumerate(top, 1):
        demo = " [demo]" if it["has_demo"] else ""
        print(f'{i:>2}. {it["score"]:>7} | ⭐{it["stars"]:<5} {it["velocity"]:>6}/д '
              f'| {it["age_days"]:>5}д | {it["full_name"]}{demo}')
        if it["desc"]:
            print(f'        {it["desc"]}')

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(top, f, ensure_ascii=False, indent=2)

    if args.telegram and top:
        send_telegram(to_telegram(top))
        con.executemany("UPDATE seen SET notified=1 WHERE full_name=?",
                        [(i["full_name"],) for i in top])
        con.commit()

    print(f"\nвсего кандидатов: {len(scored)} | база: {DB_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
