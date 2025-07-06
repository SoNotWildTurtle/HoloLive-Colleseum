import pygame

PROJECTILE_SPEED = 10

class Projectile(pygame.sprite.Sprite):
    """Simple projectile moving horizontally."""

    def __init__(self, x: int, y: int, direction: int) -> None:
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.math.Vector2(direction * PROJECTILE_SPEED, 0)

    def update(self) -> None:
        self.rect.move_ip(self.velocity.x, self.velocity.y)
