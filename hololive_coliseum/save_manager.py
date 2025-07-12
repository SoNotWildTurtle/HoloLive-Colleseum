"""Utility functions for reading and writing settings files."""

import json
import os
import shutil
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
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
            return json.load(f)
    return {}


def save_settings(data: dict[str, Any]) -> None:
    """Save settings to the `SavedGames` directory, creating it if missing."""
    path = _settings_file()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    path = _settings_file()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def wipe_saves() -> None:
    """Delete all files in the save directory if it exists."""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR, exist_ok=True)
        return
    for fname in os.listdir(SAVE_DIR):
        path = os.path.join(SAVE_DIR, fname)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    for fname in os.listdir(SAVE_DIR):
        path = os.path.join(SAVE_DIR, fname)
        try:
            os.remove(path)
        except OSError:
            pass
