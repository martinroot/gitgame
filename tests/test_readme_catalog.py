import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'gen_readme_catalog', REPO / 'scripts' / 'gen_readme_catalog.py')
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def prepare(tmp_path, monkeypatch, thumbs=('alpha.jpg', 'beta.jpg')):
    (tmp_path / 'data').mkdir()
    (tmp_path / 'data' / 'descriptions_en.json').write_text('{}')
    (tmp_path / 'thumbs').mkdir()
    for name in thumbs:
        (tmp_path / 'thumbs' / name).write_bytes(b'jpeg')
    games = [
        {'slug': 'alpha', 'title': 'Alpha', 'desc': '<b>First</b>',
         'source': 'https://github.com/x/alpha', 'thumb': ''},
        {'slug': 'beta', 'title': 'Beta', 'desc': 'Second',
         'source': 'https://github.com/x/beta', 'thumb': ''},
        {'slug': 'unrated', 'title': 'Unrated', 'desc': 'No', 'source': ''},
    ]
    (tmp_path / 'catalog.json').write_text(json.dumps(games))
    (tmp_path / 'ratings.json').write_text(json.dumps({'alpha': 4, 'beta': 5}))
    (tmp_path / 'prices.json').write_text(json.dumps({'alpha': 1.0, 'beta': 1.5}))
    monkeypatch.setattr(mod, 'ROOT', tmp_path)
    monkeypatch.setattr(mod, 'CAT', str(tmp_path / 'catalog.json'))
    monkeypatch.setattr(mod, 'RATINGS', str(tmp_path / 'ratings.json'))
    monkeypatch.setattr(mod, 'PRICES', str(tmp_path / 'prices.json'))
    monkeypatch.setattr(mod, 'THUMBS', tmp_path)
    return tmp_path / 'README.md'


def test_missing_thumbnail_aborts_generation(tmp_path, monkeypatch):
    path = prepare(tmp_path, monkeypatch, thumbs=('beta.jpg',))
    try:
        mod.main()
    except SystemExit as exc:
        assert 'missing thumbnails: alpha' in str(exc)
    else:
        raise AssertionError('main() should have failed for alpha')


def test_readme_contract(tmp_path, monkeypatch):
    path = prepare(tmp_path, monkeypatch)
    mod.main()
    md = path.read_text()
    assert md.startswith('# GitGame')
    assert md.count('<img') == 2
    assert 'No preview' not in md
    body = md.split('## Game catalog', 1)[1]
    assert '$' not in body
    assert body.index('beta.jpg') < body.index('alpha.jpg')
    assert '· [GitHub](https://github.com/x/beta)' in body
