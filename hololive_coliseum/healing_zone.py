import pygame

class HealingZone(pygame.sprite.Sprite):
    """Zone that heals players standing inside it."""

    def __init__(self, rect: pygame.Rect, heal_rate: int = 1, duration: int = 60) -> None:
        super().__init__()
        self.rect = rect
        self.heal_rate = heal_rate
        self.timer = duration
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((0, 255, 0, 80))

    def update(self) -> None:
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
