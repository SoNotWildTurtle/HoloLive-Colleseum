import json
import os
from typing import Any

SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'SavedGames')
os.makedirs(SAVE_DIR, exist_ok=True)


def _settings_file() -> str:
    return os.path.join(SAVE_DIR, 'settings.json')


def load_settings() -> dict[str, Any]:
    path = _settings_file()
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_settings(data: dict[str, Any]) -> None:
    path = _settings_file()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def wipe_saves() -> None:
    for fname in os.listdir(SAVE_DIR):
        path = os.path.join(SAVE_DIR, fname)
        try:
            os.remove(path)
        except OSError:
            pass
