import pygame

PROJECTILE_SPEED = 10
EXPLODE_TIME = 30

class Projectile(pygame.sprite.Sprite):
    """Simple projectile moving in a given direction."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        if direction.length_squared() == 0:
            direction = pygame.math.Vector2(1, 0)
        self.velocity = direction.normalize() * PROJECTILE_SPEED

    def update(self) -> None:
        self.rect.move_ip(self.velocity.x, self.velocity.y)


class ExplodingProjectile(Projectile):
    """Projectile that disappears after a short duration."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.timer = EXPLODE_TIME

    def update(self) -> None:
        super().update()
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
