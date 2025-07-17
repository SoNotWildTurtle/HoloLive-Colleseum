class ReputationManager:
    """Track faction reputation values."""
    def __init__(self):
        self.rep = {}

    def modify(self, faction: str, amount: int) -> int:
        self.rep[faction] = self.rep.get(faction, 0) + amount
        return self.rep[faction]

    def get(self, faction: str) -> int:
        return self.rep.get(faction, 0)
