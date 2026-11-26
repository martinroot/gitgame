import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'preflight_gitgame', REPO / 'scripts' / 'preflight_gitgame.py')
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def fixture(tmp_path, thumbs=('alpha.jpg', 'beta.jpg')):
    (tmp_path / 'thumbs').mkdir()
    for name in thumbs:
        (tmp_path / 'thumbs' / name).write_bytes(b'jpeg')
    games = [
        {'slug': 'alpha', 'title': 'Alpha', 'thumb': ''},
        {'slug': 'beta', 'title': 'Beta', 'thumb': 'thumbs/beta.jpg'},
        {'slug': 'unrated', 'title': 'Unrated', 'thumb': ''},
    ]
    cat = tmp_path / 'catalog.json'
    rat = tmp_path / 'ratings.json'
    cat.write_text(json.dumps(games))
    rat.write_text(json.dumps({'alpha': 4, 'beta': 5}))
    return cat, rat, tmp_path


def test_check_thumbs_happy_path(tmp_path):
    cat, rat, root = fixture(tmp_path)
    missing, checked = mod.check_thumbs(cat, rat, root)
    assert missing == []
    assert checked == 2


def test_check_thumbs_reports_missing(tmp_path):
    cat, rat, root = fixture(tmp_path, thumbs=('beta.jpg',))
    missing, checked = mod.check_thumbs(cat, rat, root)
    assert missing == ['alpha']
    assert checked == 2
