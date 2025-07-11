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


def test_wipe_saves_missing_dir(tmp_path, monkeypatch):
    target_dir = tmp_path / 'missing'
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', target_dir)
    # Directory does not exist yet
    wipe_saves()  # should recreate directory without error
    assert target_dir.exists()


def test_wipe_saves_removes_subdirs(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    sub = tmp_path / 'subdir'
    sub.mkdir()
    (sub / 'file.txt').write_text('x')
    wipe_saves()
    assert not sub.exists()
