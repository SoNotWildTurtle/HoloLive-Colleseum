class HealthManager:
    """Track and modify a character's health."""

    def __init__(self, max_health: int) -> None:
        self.max_health = max_health
        self.health = max_health

    def take_damage(self, amount: int, blocking: bool = False, parrying: bool = False) -> int:
        """Apply damage and return the new health value."""
        if parrying:
            return self.health
        if blocking:
            amount //= 2
        self.health = max(0, self.health - amount)
        return self.health

    def heal(self, amount: int) -> int:
        """Restore health and return the new value."""
        self.health = min(self.max_health, self.health + amount)
        return self.health
