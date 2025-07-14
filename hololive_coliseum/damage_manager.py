class DamageManager:
    """Compute final damage values and apply them to targets."""

    def calculate(self, base: int, defense: int = 0, multiplier: float = 1.0) -> int:
        amount = max(base - defense, 0)
        return int(amount * multiplier)

    def apply(self, target, base: int, **kwargs) -> int:
        dmg = self.calculate(base, **kwargs)
        if hasattr(target, "take_damage"):
            target.take_damage(dmg)
        return dmg
