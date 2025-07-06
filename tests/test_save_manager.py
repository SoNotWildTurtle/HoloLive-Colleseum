import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum import save_settings, load_settings, wipe_saves


def test_save_and_load_settings(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    os.makedirs(tmp_path, exist_ok=True)
    data = {"width": 123}
    save_settings(data)
    assert load_settings() == data
    wipe_saves()
    assert load_settings() == {}


def test_load_settings_handles_corrupt_file(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    os.makedirs(tmp_path, exist_ok=True)
    path = tmp_path / 'settings.json'
    path.write_text('{bad json')
    assert load_settings() == {}


def test_save_creates_directory(tmp_path, monkeypatch):
    target_dir = tmp_path / 'nested'
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', target_dir)
    data = {"test": True}
    save_settings(data)
    assert (target_dir / 'settings.json').exists()
