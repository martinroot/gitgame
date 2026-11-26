#!/bin/bash
# catalog_cleanup.sh — регламентная чистка каталога dsgame.
#
# 1) Аудит: папки без карточки в catalog.json ("не размеченные").
# 2) Проверка загрузки каждой игры (HTTP + статика; полный рендер — по --render).
# 3) Снос: битые карточки + неразмеченные папки (атомарно, с бэкапом catalog.json).
#
#   catalog_cleanup.sh            # http+static (быстро, ~1 мин)
#   catalog_cleanup.sh --render   # + полный headless-рендер (~30 мин, раз в сутки)
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

# Список битых: карточки с непустым problems
python3 - "$REPORT" <<'PY'
import json, sys
rep = json.load(open(sys.argv[1]))
bad = [r['slug'] for r in rep.get('results', []) if r.get('problems')]
open('/home/drogame/build/.catalog_bad.txt', 'w').write('\n'.join(bad))
print('битых карточек:', len(bad))
PY

# Неразмеченные папки (нет карточки) — через purge --unmarked
if [ -s /home/drogame/build/.catalog_bad.txt ]; then
    python3 catalog_purge.py --slugs-file /home/drogame/build/.catalog_bad.txt
fi
python3 catalog_purge.py --unmarked

rm -f /home/drogame/build/.catalog_bad.txt
echo "[$STAMP] готово"
