import pygame

GRAVITY = 0.5
JUMP_VELOCITY = -10
MOVE_SPEED = 5


class Player(pygame.sprite.Sprite):
    """Simple rectangular player with basic platformer physics."""

    def __init__(self, x: int, y: int, color=(255, 255, 255)) -> None:
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False

    def handle_input(self, keys) -> None:
        if keys[pygame.K_LEFT]:
            self.velocity.x = -MOVE_SPEED
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = MOVE_SPEED
        else:
            self.velocity.x = 0
        if self.on_ground and keys[pygame.K_SPACE]:
            self.velocity.y = JUMP_VELOCITY
            self.on_ground = False

    def apply_gravity(self) -> None:
        self.velocity.y += GRAVITY

    def update(self, ground_y: int) -> None:
        self.apply_gravity()
        self.pos += self.velocity
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.pos.y = self.rect.top
            self.velocity.y = 0
            self.on_ground = True

