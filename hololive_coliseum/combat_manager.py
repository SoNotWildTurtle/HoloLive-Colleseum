class CombatManager:
    """Handle basic turn order and engagement logic."""

    def __init__(self) -> None:
        self.participants: list = []
        self.index = 0

    def add(self, actor) -> None:
        """Add a combatant to the turn list."""
        self.participants.append(actor)

    def remove(self, actor) -> None:
        if actor in self.participants:
            self.participants.remove(actor)

    def next_actor(self):
        """Return the next actor in the turn order."""
        if not self.participants:
            return None
        actor = self.participants[self.index % len(self.participants)]
        self.index += 1
        return actor
