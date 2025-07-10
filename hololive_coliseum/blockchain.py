import json
import os
import time
import uuid
import hashlib
from typing import Any, Dict, List

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


def _hash_block(data: Dict[str, Any]) -> str:
    raw = json.dumps(data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def add_game(players: List[str], winner: str, bet: int = 0, game_id: str | None = None) -> Dict[str, Any]:
    """Append a new game result to the blockchain and update balances."""
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
