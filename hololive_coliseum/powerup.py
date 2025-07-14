import pygame

class PowerUp(pygame.sprite.Sprite):
    """Simple powerup that restores health or mana."""

    def __init__(self, x: int, y: int, effect: str) -> None:
        super().__init__()
        self.effect = effect
        self.image = pygame.Surface((20, 20))
        color = (0, 255, 0) if effect == "heal" else (0, 0, 255)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
