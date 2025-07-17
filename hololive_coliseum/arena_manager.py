class ArenaManager:
    """Handle PvP arena rankings and rewards."""

    def __init__(self):
        self.scores = {}

    def record_win(self, player: str) -> None:
        self.scores[player] = self.scores.get(player, 0) + 1

    def top_player(self):
        return max(self.scores, key=self.scores.get) if self.scores else None
