import importlib.util
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / 'scripts' / 'gen_readme_catalog.py'
spec = importlib.util.spec_from_file_location('gen_readme_catalog', MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def make_thumbs(tmp_path):
    (tmp_path / 'thumbs').mkdir()
    (tmp_path / 'thumbs' / 'alpha.jpg').write_bytes(b'jpeg')
    (tmp_path / 'thumbs' / 'beta.jpg').write_bytes(b'jpeg')
    return tmp_path


def test_empty_catalog_thumb_falls_back_to_slug_jpg(tmp_path):
    assert mod.image_url('beta', '', make_thumbs(tmp_path)) == \
        'https://gitgame.live/thumbs/beta.jpg'


def test_explicit_catalog_thumb_is_used(tmp_path):
    assert mod.image_url('alpha', 'thumbs/alpha.jpg', make_thumbs(tmp_path)) == \
        'https://gitgame.live/thumbs/alpha.jpg'


def test_missing_file_returns_none(tmp_path):
    assert mod.image_url('gamma', 'thumbs/gamma.jpg', make_thumbs(tmp_path)) is None
