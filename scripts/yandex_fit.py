#!/usr/bin/env python3
"""
yandex_fit.py — 2-й этап радара: оценка пригодности репы к Яндекс.Играм.

Берёт кандидатов из out.json (вывод vibegame_radar.py), дообогащает каждую
репу через GitHub API (лицензия, языки, корневые файлы, package.json, README)
и считает «Yandex Fitness» — насколько легко довести игру до публикации на
Яндекс.Играх (статика в zip + Yandex Games SDK) и монетизировать рекламой.

Запуск:
  export GITHUB_TOKEN=ghp_...
  python3 yandex_fit.py --in out.json --top 10
  python3 yandex_fit.py --in out.json --json fit.json
"""

import argparse
import base64
import json
import os
import re
import sys
import time

import requests

API = "https://api.github.com"

PERMISSIVE = {"MIT", "APACHE-2.0", "BSD-2-CLAUSE", "BSD-3-CLAUSE", "ISC",
              "UNLICENSE", "CC0-1.0", "0BSD", "ZLIB", "MPL-2.0"}
COPYLEFT = {"GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-3.0", "LGPL-2.1"}

# зависимости/файлы, означающие ОБЯЗАТЕЛЬНЫЙ серверный бэкенд (Яндекс хостит только статику)
SERVER_DEPS = {"socket.io", "ws", "express", "fastify", "koa", "colyseus",
               "@colyseus/core", "socket.io-server", "uWebSockets.js", "hapi", "nakama-js"}
SERVER_FILES = {"server.js", "server.ts", "server.py", "app.py", "main.py",
                "go.mod", "cargo.toml", "gemfile", "composer.json", "manage.py",
                "docker-compose.yml", "docker-compose.yaml", "procfile"}
CLIENT_ENGINES = {"three", "@react-three/fiber", "phaser", "pixi.js", "babylonjs",
                  "@babylonjs/core", "aframe", "playcanvas", "kaboom", "kaplay", "excalibur"}

# жанры → монетизационный профиль (рекламой на Яндексе)
GENRE_GOOD = ["runner", "arcade", "racing", "kart", "tower defense", "tower-defense",
              "hyper-casual", "hypercasual", "casual", "puzzle", "clicker", "idle",
              "endless", "flappy", "crossy", "match-3", "shooter", ".io"]
GENRE_HARD = ["rpg", "mmo", "simulator", "sandbox", "open world", "open-world",
              "strategy", "roguelike", "metroidvania"]


def gh(path, token, params=None):
    h = {"Accept": "application/vnd.github+json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    for attempt in range(4):
        r = requests.get(f"{API}{path}", headers=h, params=params, timeout=30)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 404:
            return None
        if r.status_code in (403, 429):
            reset = int(r.headers.get("x-ratelimit-reset", 0))
            wait = max(3, min(60, reset - int(time.time()) + 2)) if reset else 10 * (attempt + 1)
            print(f"    rate limit, sleep {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        return None
    return None


def fetch_text(path, token):
    d = gh(path, token)
    if not d or "content" not in d:
        return ""
    try:
        return base64.b64decode(d["content"]).decode("utf-8", "ignore")
    except Exception:
        return ""


def enrich(full_name, token):
    meta = gh(f"/repos/{full_name}", token) or {}
    langs = gh(f"/repos/{full_name}/languages", token) or {}
    contents = gh(f"/repos/{full_name}/contents", token) or []
    root_files = {c["name"].lower(): c for c in contents} if isinstance(contents, list) else {}

    # license
    lic = ((meta.get("license") or {}).get("spdx_id") or "NOASSERTION").upper()
    if lic in ("NOASSERTION", "NONE", ""):
        lic_ok, lic_note = False, "нет лицензии — юридически публиковать нельзя"
    elif lic in PERMISSIVE:
        lic_ok, lic_note = True, f"{lic} — можно форкать и коммерциализировать"
    elif lic in COPYLEFT:
        lic_ok, lic_note = True, f"{lic} — copyleft, обязаны открыть исходники"
    else:
        lic_ok, lic_note = False, f"{lic} — проверить условия вручную"

    # package.json → deps
    deps = {}
    if "package.json" in root_files:
        pj = fetch_text(f"/repos/{full_name}/contents/package.json", token)
        try:
            j = json.loads(pj)
            deps = {**j.get("dependencies", {}), **j.get("devDependencies", {})}
        except Exception:
            pass
    dep_names = {d.lower() for d in deps}

    # backend?
    server_hits = ([f for f in SERVER_FILES if f in root_files] +
                   [d for d in SERVER_DEPS if d.lower() in dep_names] +
                   [l for l in langs if l in ("Python", "Go", "Rust", "PHP", "Ruby", "Java", "C#")])
    backend_required = bool(server_hits)

    # client engine
    engine = next((e for e in CLIENT_ENGINES if e.lower() in dep_names), None)
    if not engine:
        for e in ("three", "phaser", "babylon", "pixi", "aframe", "webgl", "webgpu"):
            if any(e in (t or "").lower() for t in meta.get("topics", [])):
                engine = e
                break

    # static buildable?
    has_index = "index.html" in root_files
    has_vite = "vite.config.js" in root_files or "vite.config.ts" in root_files or "vite" in dep_names
    static_ok = has_index or has_vite
    build_note = ("готовый index.html — статика из коробки" if has_index
                  else "Vite → npm run build даёт статику" if has_vite
                  else "нет явной статики/сборки — паковать сложнее")

    # README + описание для эвристик
    readme = fetch_text(f"/repos/{full_name}/readme", token).lower()
    desc = (meta.get("description") or "").lower()
    topics = " ".join(meta.get("topics") or []).lower()
    blob = " ".join([desc, topics, readme[:4000]])

    self_contained = any(k in blob for k in
                         ["procedural", "no external", "no third-party", "no assets",
                          "generated at runtime", "single html", "one html file",
                          "no build step", "no cdn", "процедурн"])
    mobile = any(k in blob for k in
                 ["touch", "mobile", "responsive", "portrait", "мобил", "тач"])
    yandex_ready = "yandex" in blob or "яндекс" in blob

    genre_good = any(g in blob for g in GENRE_GOOD)
    genre_hard = any(g in blob for g in GENRE_HARD)

    size_kb = meta.get("size", 0)

    # ---------- scoring ----------
    score = 0
    reasons, flags = [], []

    if lic_ok and lic in PERMISSIVE:
        score += 25; reasons.append(f"лицензия {lic}")
    elif lic_ok:
        score += 10; reasons.append(lic_note)
    else:
        flags.append(lic_note)

    if backend_required:
        flags.append(f"нужен бэкенд ({', '.join(server_hits[:3])}) — Яндекс хостит только статику")
    else:
        score += 20; reasons.append("клиентская, без обязательного сервера")

    if static_ok:
        score += 15; reasons.append(build_note)
    else:
        flags.append(build_note)

    if self_contained:
        score += 15; reasons.append("self-contained ассеты (процедурные/забандлены)")
    if mobile:
        score += 12; reasons.append("есть тач/мобайл")
    else:
        flags.append("не видно тач-управления — трафик Яндекса в основном мобильный")

    if genre_good:
        score += 10; reasons.append("жанр хорошо монетизируется рекламой (аркада/казуалка)")
    if genre_hard:
        score -= 8; flags.append("тяжёлый жанр (RPG/симулятор) — реклама монетизирует слабее")

    if yandex_ready:
        score += 6; reasons.append("уже упоминается Яндекс/SDK")

    if 0 < size_kb < 20000:
        score += 5; reasons.append(f"компактная репа (~{size_kb} KB)")
    elif size_kb >= 100000:
        score -= 5; flags.append(f"тяжёлая репа (~{size_kb} KB)")

    score = max(0, min(100, score))
    if score >= 70:
        verdict = "🟢 брать"
    elif score >= 45:
        verdict = "🟡 можно, есть работа"
    else:
        verdict = "🔴 дорого/нельзя"

    return {
        "full_name": full_name,
        "fitness": score,
        "verdict": verdict,
        "license": lic,
        "backend_required": backend_required,
        "engine": engine,
        "static_ok": static_ok,
        "self_contained": self_contained,
        "mobile": mobile,
        "genre_good": genre_good,
        "size_kb": size_kb,
        "reasons": reasons,
        "flags": flags,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="out.json")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--json", metavar="PATH")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    with open(args.inp, encoding="utf-8") as f:
        cands = json.load(f)[: args.top]

    out = []
    for c in cands:
        fn = c["full_name"]
        print(f"[fit] {fn}", file=sys.stderr)
        row = enrich(fn, token)
        row["hype_score"] = c.get("score")
        row["stars"] = c.get("stars")
        row["velocity"] = c.get("velocity")
        row["has_demo"] = c.get("has_demo")
        row["url"] = c.get("url")
        out.append(row)
        time.sleep(0.5)

    out.sort(key=lambda x: -x["fitness"])

    for r in out:
        print(f'\n{r["verdict"]}  fitness {r["fitness"]}  | hype {r["hype_score"]} '
              f'⭐{r["stars"]} | {r["full_name"]}')
        print(f'   движок:{r["engine"] or "?"}  лиц:{r["license"]}  '
              f'бэкенд:{"ДА" if r["backend_required"] else "нет"}  '
              f'статика:{"да" if r["static_ok"] else "нет"}  '
              f'мобайл:{"да" if r["mobile"] else "нет"}  demo:{"да" if r["has_demo"] else "нет"}')
        if r["reasons"]:
            print("   + " + "; ".join(r["reasons"]))
        if r["flags"]:
            print("   ! " + "; ".join(r["flags"]))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"\nсохранено: {args.json}", file=sys.stderr)


if __name__ == "__main__":
    main()
