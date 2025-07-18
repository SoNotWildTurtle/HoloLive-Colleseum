import pygame

class SpikeTrap(pygame.sprite.Sprite):
    """Rectangular hazard that damages sprites on contact."""

    def __init__(self, rect: pygame.Rect, damage: int = 10) -> None:
        super().__init__()
        self.rect = rect
        self.damage = damage
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((200, 0, 0))
        self.avoid = True

class IceZone(pygame.sprite.Sprite):
    """Zone with slippery surface reducing friction."""

    def __init__(self, rect: pygame.Rect, friction: float = 0.5) -> None:
        super().__init__()
        self.rect = rect
        self.friction = friction
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill((0, 200, 255, 80))
        self.avoid = False
