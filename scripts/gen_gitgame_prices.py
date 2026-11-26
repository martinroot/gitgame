#!/usr/bin/env python3
"""Emit slug -> USD price map for GitGame checkout (server-side price lookup)."""
import json
import os
import sys

sys.path.insert(0, '/home/drogame/build')
import gitgame_gen

games = gitgame_gen.load()
prices = {g['slug']: round(float(g['price']), 2) for g in games}
out = '/var/www/gitgame.live/api/prices.json'
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w') as f:
    json.dump(prices, f, sort_keys=True)
os.chmod(out, 0o644)
print(f'{out}: {len(prices)} games, sample:', dict(list(prices.items())[:3]))
