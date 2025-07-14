"""User account registry storing public keys and access levels."""

from __future__ import annotations

import json
import os
from typing import Any, Dict

SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'SavedGames')
os.makedirs(SAVE_DIR, exist_ok=True)
ACCOUNTS_FILE = os.path.join(SAVE_DIR, 'accounts.json')


def _load_json(path: str, default: Any) -> Any:
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return default
    return default


def _save_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def load_accounts() -> Dict[str, Dict[str, str]]:
    """Return saved account data mapping user IDs to level and public key."""
    return _load_json(ACCOUNTS_FILE, {})


def save_accounts(data: Dict[str, Dict[str, str]]) -> None:
    _save_json(ACCOUNTS_FILE, data)


def register_account(user_id: str, level: str, public_key_pem: str) -> None:
    accounts = load_accounts()
    accounts[user_id] = {"level": level, "public_key": public_key_pem}
    save_accounts(accounts)


def delete_account(user_id: str) -> None:
    """Remove ``user_id`` from the registry if present."""
    accounts = load_accounts()
    if user_id in accounts:
        del accounts[user_id]
        save_accounts(accounts)


def get_account(user_id: str) -> Dict[str, str] | None:
    return load_accounts().get(user_id)
