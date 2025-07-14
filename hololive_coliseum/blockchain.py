import json
import os
import time
import uuid
import hashlib
import base64
from typing import Any, Dict, List

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from .accounts import get_account

# Path to SavedGames directory used by save_manager
SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'SavedGames')
os.makedirs(SAVE_DIR, exist_ok=True)
CHAIN_FILE = os.path.join(SAVE_DIR, 'chain.json')
BALANCE_FILE = os.path.join(SAVE_DIR, 'balances.json')
CONTRACT_FILE = os.path.join(SAVE_DIR, 'contracts.json')


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


def load_chain() -> List[Dict[str, Any]]:
    """Return the saved blockchain."""
    return _load_json(CHAIN_FILE, [])


def save_chain(chain: List[Dict[str, Any]]) -> None:
    _save_json(CHAIN_FILE, chain)


def load_balances() -> Dict[str, int]:
    return _load_json(BALANCE_FILE, {})


def save_balances(data: Dict[str, int]) -> None:
    _save_json(BALANCE_FILE, data)


def get_balance(user_id: str) -> int:
    """Return the stored balance for ``user_id`` or ``0`` if missing."""
    balances = load_balances()
    return balances.get(user_id, 0)




def _hash_block(data: Dict[str, Any]) -> str:
    raw = json.dumps(data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def add_game(players: List[str], winner: str, bet: int = 0, game_id: str | None = None) -> Dict[str, Any]:
    """Append a new game result to the blockchain and update balances.

    Each ``player`` must exist in the account registry or a ``ValueError`` is
    raised.
    """
    for p in players:
        if get_account(p) is None:
            raise ValueError(f"unknown account: {p}")
    chain = load_chain()
    prev_hash = chain[-1]['hash'] if chain else ''
    if game_id is None:
        game_id = uuid.uuid4().hex
    block = {
        'index': len(chain),
        'game_id': game_id,
        'players': players,
        'winner': winner,
        'bet': bet,
        'timestamp': int(time.time()),
        'prev_hash': prev_hash,
    }
    block['hash'] = _hash_block(block)
    chain.append(block)
    save_chain(chain)

    if bet:
        balances = load_balances()
        for p in players:
            balances[p] = balances.get(p, 0) - bet
        balances[winner] = balances.get(winner, 0) + bet * len(players)
        save_balances(balances)
    return block


def search(game_id: str | None = None, user_id: str | None = None) -> List[Dict[str, Any]]:
    """Search blocks by game ID and/or user ID."""
    chain = load_chain()
    results = chain
    if game_id is not None:
        results = [b for b in results if b['game_id'] == game_id]
    if user_id is not None:
        results = [b for b in results if user_id in b['players']]
    return results


def add_contract(request_id: str, players: List[str], bet: int) -> None:
    contracts = _load_json(CONTRACT_FILE, {})
    contracts[request_id] = {'players': players, 'bet': bet}
    _save_json(CONTRACT_FILE, contracts)


def fulfill_contract(request_id: str, winner: str) -> Dict[str, Any] | None:
    contracts = _load_json(CONTRACT_FILE, {})
    contract = contracts.pop(request_id, None)
    if contract is None:
        return None
    _save_json(CONTRACT_FILE, contracts)
    return add_game(contract['players'], winner, contract['bet'], game_id=request_id)


def verify_chain(chain: List[Dict[str, Any]]) -> bool:
    """Return True if the chain hashes link correctly."""
    prev_hash = ''
    for block in chain:
        expect = _hash_block({k: block[k] for k in block if k != 'hash'})
        if block.get('prev_hash') != prev_hash or block.get('hash') != expect:
            return False
        prev_hash = block['hash']
    return True


def merge_chain(remote: List[Dict[str, Any]]) -> None:
    """Merge a remote chain with the local one if it is valid and longer."""
    if not verify_chain(remote):
        return
    local = load_chain()
    if len(remote) > len(local):
        save_chain(remote)


def add_message(
    sender: str,
    recipient: str,
    message: str,
    admin_public_key_pem: bytes,
) -> Dict[str, Any]:
    """Encrypt ``message`` for ``recipient`` and append it as a block.

    The message is encrypted with a random symmetric key. That key is encrypted
    twice: once with the recipient's public key and once with the admin key so
    moderators can decrypt abusive messages if necessary.
    """
    recipient_info = get_account(recipient)
    if recipient_info is None:
        raise ValueError("unknown recipient")

    rec_pub = serialization.load_pem_public_key(
        recipient_info["public_key"].encode("utf-8")
    )
    admin_pub = serialization.load_pem_public_key(admin_public_key_pem)

    sym_key = Fernet.generate_key()
    cipher = Fernet(sym_key).encrypt(message.encode("utf-8"))

    enc_rec = rec_pub.encrypt(
        sym_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    enc_admin = admin_pub.encrypt(
        sym_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )

    chain = load_chain()
    prev_hash = chain[-1]["hash"] if chain else ""
    block = {
        "index": len(chain),
        "type": "message",
        "sender": sender,
        "recipient": recipient,
        "cipher": base64.b64encode(cipher).decode("ascii"),
        "key_user": base64.b64encode(enc_rec).decode("ascii"),
        "key_admin": base64.b64encode(enc_admin).decode("ascii"),
        "timestamp": int(time.time()),
        "prev_hash": prev_hash,
    }
    block["hash"] = _hash_block(block)
    chain.append(block)
    save_chain(chain)
    return block


def decrypt_message(block: Dict[str, Any], private_key_pem: bytes) -> str:
    """Return the plaintext of ``block`` using the recipient's private key."""
    if block.get("type") != "message":
        raise ValueError("not a message block")
    priv = serialization.load_pem_private_key(private_key_pem, password=None)
    sym_key = priv.decrypt(
        base64.b64decode(block["key_user"]),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    return Fernet(sym_key).decrypt(base64.b64decode(block["cipher"])).decode("utf-8")


def admin_decrypt(block: Dict[str, Any], admin_private_key_pem: bytes) -> str:
    """Decrypt a message block using the admin private key."""
    if block.get("type") != "message":
        raise ValueError("not a message block")
    priv = serialization.load_pem_private_key(admin_private_key_pem, password=None)
    sym_key = priv.decrypt(
        base64.b64decode(block["key_admin"]),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    return Fernet(sym_key).decrypt(base64.b64decode(block["cipher"])).decode("utf-8")
