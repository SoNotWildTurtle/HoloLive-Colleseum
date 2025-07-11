from __future__ import annotations

from typing import Any, Dict

class StateSync:
    """Compute diffs between game state snapshots for efficient networking."""

    def __init__(self) -> None:
        self.last_state: Dict[str, Any] = {}
        self.seq: int = 0

    def encode(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Return the delta from the previous state with a sequence number."""
        self.seq += 1
        delta = {k: v for k, v in state.items() if self.last_state.get(k) != v}
        delta["seq"] = self.seq
        self.last_state = state.copy()
        return delta

    def apply(self, delta: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a delta update and return the resulting state."""
        if 'seq' in delta:
            self.seq = delta['seq']
        for k, v in delta.items():
            if k == 'seq':
                continue
            self.last_state[k] = v
        return self.last_state.copy()
