import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum import (
    load_chain,
    add_game,
    search,
    add_contract,
    fulfill_contract,
    load_balances,
)


def test_add_and_search(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')

    block = add_game(['alice', 'bob'], 'alice', bet=5, game_id='g1')
    assert block['index'] == 0
    assert search(game_id='g1')[0]['winner'] == 'alice'

    balances = load_balances()
    assert balances['alice'] == 5
    assert balances['bob'] == -5


def test_contract_flow(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')

    add_contract('req1', ['a', 'b'], 2)
    block = fulfill_contract('req1', 'b')
    assert block['game_id'] == 'req1'
    chain = load_chain()
    assert len(chain) == 1
    assert chain[0]['winner'] == 'b'
