import os
import sys
import pygame

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum import load_accounts, register_account, delete_account


def test_register_and_delete_account(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'a.json')
    os.makedirs(tmp_path, exist_ok=True)
    register_account('alice', 'user', 'PUB')
    assert load_accounts() == {'alice': {'level': 'user', 'public_key': 'PUB'}}
    delete_account('alice')
    assert load_accounts() == {}


def test_execute_account_option(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'b.json')
    from hololive_coliseum.game import Game

    game = Game()
    game.account_id = 'bob'
    game.execute_account_option('Register Account')
    assert load_accounts() == {'bob': {'level': 'user', 'public_key': 'PUBKEY'}}
    game.execute_account_option('Delete Account')
    assert load_accounts() == {}
    pygame.quit()
