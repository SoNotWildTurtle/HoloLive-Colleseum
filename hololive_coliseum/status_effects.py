import pygame

class StatusEffect:
    """Base status effect applied to a sprite."""

    def __init__(self, duration_ms: int) -> None:
        self.start_time = pygame.time.get_ticks()
        self.end_time = self.start_time + duration_ms

    def apply(self, target):
        pass

    def update(self, target):
        pass

    def remove(self, target):
        pass


class FreezeEffect(StatusEffect):
    """Halve target speed for a short duration."""

    def __init__(self, duration_ms: int = 1000, factor: float = 0.5) -> None:
        super().__init__(duration_ms)
        self.factor = factor

    def apply(self, target):
        if hasattr(target, "speed_factor"):
            target.speed_factor *= self.factor
        target.velocity.x *= self.factor
        target.velocity.y *= self.factor

    def remove(self, target):
        if hasattr(target, "speed_factor"):
            target.speed_factor /= self.factor


class SlowEffect(StatusEffect):
    """Reduce horizontal speed of the target."""

    def __init__(self, duration_ms: int = 1000, factor: float = 0.5) -> None:
        super().__init__(duration_ms)
        self.factor = factor

    def apply(self, target):
        if hasattr(target, "speed_factor"):
            target.speed_factor *= self.factor
        target.velocity.x *= self.factor

    def remove(self, target):
        if hasattr(target, "speed_factor"):
            target.speed_factor /= self.factor


class StatusEffectManager:
    """Keep track of active status effects on sprites."""

    def __init__(self) -> None:
        self._effects: list[tuple[object, StatusEffect]] = []

    def add_effect(self, target, effect: StatusEffect) -> None:
        effect.apply(target)
        self._effects.append((target, effect))

    def update(self, now: int | None = None) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        for target, effect in list(self._effects):
            if now >= effect.end_time:
                effect.remove(target)
                self._effects.remove((target, effect))
            else:
                effect.update(target)
