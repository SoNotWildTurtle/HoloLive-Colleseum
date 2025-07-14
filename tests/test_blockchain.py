import os
import sys
import json
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hololive_coliseum import (
    load_chain,
    add_game,
    search,
    add_contract,
    fulfill_contract,
    load_balances,
    verify_chain,
    merge_chain,
    register_account,
    load_accounts,
    add_message,
    decrypt_message,
    admin_decrypt,
)


def test_add_and_search(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'accounts.json')

    register_account('alice', 'user', 'pubA')
    register_account('bob', 'user', 'pubB')
    block = add_game(['alice', 'bob'], 'alice', bet=5, game_id='g1')
    assert block['index'] == 0
    assert search(game_id='g1')[0]['winner'] == 'alice'

    balances = load_balances()
    assert balances['alice'] == 5
    assert balances['bob'] == -5
    from hololive_coliseum.blockchain import get_balance
    assert get_balance('alice') == 5
    assert get_balance('bob') == -5


def test_contract_flow(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'accounts.json')

    register_account('a', 'user', 'pubA')
    register_account('b', 'user', 'pubB')
    add_contract('req1', ['a', 'b'], 2)
    block = fulfill_contract('req1', 'b')
    assert block['game_id'] == 'req1'
    chain = load_chain()
    assert len(chain) == 1
    assert chain[0]['winner'] == 'b'


def test_verify_and_merge(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'accounts.json')

    register_account('a', 'user', 'pubA')
    register_account('b', 'user', 'pubB')
    local = [add_game(['a'], 'a', game_id='g1')]
    assert verify_chain(local)
    remote = local + [
        {
            'index': 1,
            'game_id': 'g2',
            'players': ['a', 'b'],
            'winner': 'b',
            'bet': 0,
            'timestamp': local[0]['timestamp'] + 1,
            'prev_hash': local[0]['hash'],
        }
    ]
    remote[1]['hash'] = hashlib.sha256(json.dumps(remote[1], sort_keys=True).encode('utf-8')).hexdigest()
    merge_chain(remote)
    assert len(load_chain()) == 2


def test_message_encryption(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.blockchain.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.blockchain.CHAIN_FILE', tmp_path / 'c.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.BALANCE_FILE', tmp_path / 'b.json')
    monkeypatch.setattr('hololive_coliseum.blockchain.CONTRACT_FILE', tmp_path / 'contracts.json')
    monkeypatch.setattr('hololive_coliseum.accounts.SAVE_DIR', tmp_path)
    monkeypatch.setattr('hololive_coliseum.accounts.ACCOUNTS_FILE', tmp_path / 'accounts.json')

    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization

    admin_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    admin_pub = admin_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    user_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    user_pub = user_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    register_account('bob', 'user', user_pub.decode('ascii'))
    block = add_message('alice', 'bob', 'hello', admin_pub)

    msg_user = decrypt_message(block, user_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ))
    msg_admin = admin_decrypt(block, admin_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ))
    assert msg_user == 'hello'
    assert msg_admin == 'hello'
