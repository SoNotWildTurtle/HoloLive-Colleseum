import pygame

PROJECTILE_SPEED = 10
EXPLODE_TIME = 30

class Projectile(pygame.sprite.Sprite):
    """Simple projectile moving in a given direction."""

    def __init__(
        self,
        x: int,
        y: int,
        direction: pygame.math.Vector2,
        from_enemy: bool = False,
    ) -> None:

class Projectile(pygame.sprite.Sprite):
    """Simple projectile moving horizontally."""

    def __init__(self, x: int, y: int, direction: int) -> None:
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.from_enemy = from_enemy
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


class GrappleProjectile(Projectile):
    """Projectile that pulls enemies toward the shooter on contact."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.grapple = True


class BoomerangProjectile(Projectile):
    """Projectile that returns to the shooter after a short delay."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2, owner) -> None:
        super().__init__(x, y, direction)
        self.owner = owner
        self.timer = 15

    def update(self) -> None:
        if self.timer > 0:
            self.timer -= 1
        else:
            to_owner = pygame.math.Vector2(
                self.owner.rect.centerx - self.rect.centerx,
                self.owner.rect.centery - self.rect.centery,
            )
            if to_owner.length_squared() > 0:
                self.velocity = to_owner.normalize() * PROJECTILE_SPEED
        super().update()
        if self.rect.colliderect(self.owner.rect):
            self.kill()


class ExplosionProjectile(Projectile):
    """Short-lived projectile that damages enemies in an area."""

    def __init__(self, x: int, y: int, radius: int = 30) -> None:
        super().__init__(x, y, pygame.math.Vector2(0, 0))
        self.radius = radius
        self.timer = 5
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 128, 0), (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self) -> None:
        self.timer -= 1
        if self.timer <= 0:
            self.kill()


class FreezingProjectile(Projectile):
    """Projectile that slows enemies on hit."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.freeze = True
        self.image.fill((200, 255, 255))


class FlockProjectile(Projectile):
    """Projectile that slows enemies by summoning a flock."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.slow = True
        self.image.fill((150, 150, 255))


class PiercingProjectile(Projectile):
    """Projectile that passes through enemies instead of disappearing."""

    def __init__(self, x: int, y: int, direction: pygame.math.Vector2) -> None:
        super().__init__(x, y, direction)
        self.pierce = True
        self.image.fill((255, 105, 180))

        self.velocity = pygame.math.Vector2(direction * PROJECTILE_SPEED, 0)

    def update(self) -> None:
        self.rect.move_ip(self.velocity.x, self.velocity.y)
