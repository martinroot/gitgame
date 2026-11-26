#!/bin/bash
#catalog_cleanup.sh — scheduled cleanup of the dsgame catalog.
#
#1) Audit: folders without a card in catalog.json ("unmarked").
#2) Check loading of each game (HTTP + static; full render via --render).
#3) Purge: broken cards + unmarked folders (atomically, with a catalog.json backup).
#
#catalog_cleanup.sh            # http+static (fast, ~1 min)
#catalog_cleanup.sh --render   # + full headless render (~30 min, once a day)
set -uo pipefail
cd /home/drogame/build
exec 9>/home/drogame/build/.catalog_cleanup.lock
flock -n 9 || exit 0

LEVEL=static
[ "${1:-}" = "--render" ] && LEVEL=render

REPORT=/home/drogame/build/catalog_cleanup_report.json
STAMP=$(date +%Y%m%d-%H%M%S)

echo "[$STAMP] проверка уровня=$LEVEL"
python3 catalog_verify.py --level "$LEVEL" --workers 4 --out "$REPORT" 2>&1 | tail -30

#Broken list: cards with non-empty problems
python3 - "$REPORT" <<'PY'
import json, sys
rep = json.load(open(sys.argv[1]))
bad = [r['slug'] for r in rep.get('results', []) if r.get('problems')]
open('/home/drogame/build/.catalog_bad.txt', 'w').write('\n'.join(bad))
print('битых карточек:', len(bad))
PY

#Unmarked folders (no card) — via purge --unmarked
if [ -s /home/drogame/build/.catalog_bad.txt ]; then
    python3 catalog_purge.py --slugs-file /home/drogame/build/.catalog_bad.txt
fi
python3 catalog_purge.py --unmarked

rm -f /home/drogame/build/.catalog_bad.txt
echo "[$STAMP] готово"
