import pygame

MELEE_LIFETIME = 10  # frames
MELEE_SIZE = (30, 20)


class MeleeAttack(pygame.sprite.Sprite):
    """Temporary hitbox representing a melee swing."""

    def __init__(
        self, x: int, y: int, facing: int, from_enemy: bool = False
    ) -> None:
    def __init__(self, x: int, y: int, facing: int) -> None:
        super().__init__()
        self.image = pygame.Surface(MELEE_SIZE, pygame.SRCALPHA)
        self.image.fill((255, 255, 0))  # yellow
        # Position attack in front of the player
        if facing >= 0:
            self.rect = self.image.get_rect(midleft=(x, y))
        else:
            self.rect = self.image.get_rect(midright=(x, y))
        self.lifetime = MELEE_LIFETIME
        self.from_enemy = from_enemy

    def update(self) -> None:
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
