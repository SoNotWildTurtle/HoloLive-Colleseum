class ExperienceManager:
    """Handle experience gain and leveling."""

    def __init__(self, level: int = 1, xp: int = 0, threshold: int = 100) -> None:
        self.level = level
        self.xp = xp
        self.threshold = threshold

    def add_xp(self, amount: int) -> bool:
        """Add experience and return True if a level-up occurred."""
        self.xp += amount
        leveled = False
        while self.xp >= self.threshold:
            self.xp -= self.threshold
            self.level += 1
            leveled = True
        return leveled
