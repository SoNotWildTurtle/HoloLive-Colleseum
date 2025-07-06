from __future__ import annotations
import os
import pygame

GRAVITY = 0.5
JUMP_VELOCITY = -10
MOVE_SPEED = 5
PROJECTILE_COOLDOWN = 250  # milliseconds
MELEE_COOLDOWN = 500  # milliseconds
PARRY_COOLDOWN = 1000  # milliseconds
PARRY_DURATION = 200  # milliseconds
SPECIAL_COOLDOWN = 1000  # milliseconds


class Player(pygame.sprite.Sprite):
    """Simple player sprite that can load an image or use a colored rectangle."""

    def __init__(
        self, x: int, y: int, image_path: str | None = None, color=(255, 255, 255)
    ) -> None:
        super().__init__()
        if image_path:
            if os.path.exists(image_path):
                self.image = pygame.image.load(image_path).convert_alpha()
            else:
                self.image = pygame.Surface((64, 64))
                self.image.fill(color)
        else:
            self.image = pygame.Surface((40, 60))
            self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.direction = 1  # 1 for right, -1 for left
        self.last_shot = 0
        self.last_melee = -MELEE_COOLDOWN
        self.last_parry = -PARRY_COOLDOWN
        self.parrying = False
        self.gravity_multiplier = 1.0
        self.max_health = 100
        self.health = self.max_health
        self.max_mana = 100
        self.mana = self.max_mana
        self.blocking = False
        
    def handle_input(self, keys, now: int | None = None, key_bindings: dict[str, int] | None = None) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        if keys[pygame.K_LEFT]:
            self.velocity.x = -MOVE_SPEED
            self.direction = -1
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = MOVE_SPEED
            self.direction = 1
        else:
            self.velocity.x = 0
        if key_bindings is None:
            key_bindings = {
                "block": pygame.K_LSHIFT,
                "parry": pygame.K_c,
                "jump": pygame.K_SPACE,
            }
        self.blocking = keys[key_bindings.get("block", pygame.K_LSHIFT)]
        if keys[key_bindings.get("parry", pygame.K_c)]:
            self.parry(now)
        if self.on_ground and keys[key_bindings.get("jump", pygame.K_SPACE)]:
            self.velocity.y = JUMP_VELOCITY
            self.on_ground = False

    def shoot(self, now: int):
        """Return a projectile if the cooldown has elapsed."""
        from .projectile import Projectile

        if now - self.last_shot >= PROJECTILE_COOLDOWN and self.use_mana(10):
            self.last_shot = now
            x = self.rect.centerx + self.direction * 20
            y = self.rect.centery
            return Projectile(x, y, self.direction)
        return None

    def melee_attack(self, now: int):
        """Return a melee attack sprite if cooldown allows."""
        from .melee_attack import MeleeAttack

        if now - self.last_melee >= MELEE_COOLDOWN:
            self.last_melee = now
            x = self.rect.centerx + self.direction * 20
            y = self.rect.centery
            return MeleeAttack(x, y, self.direction)
        return None

    def special_attack(self, now: int):
        """Return a special projectile if available. Base players have none."""
        return None

    def parry(self, now: int) -> bool:
        """Start a parry if cooldown allows."""
        if now - self.last_parry >= PARRY_COOLDOWN:
            self.last_parry = now
            self.parrying = True
            return True
        return False

    def apply_gravity(self) -> None:
        self.velocity.y += GRAVITY * self.gravity_multiplier

    def take_damage(self, amount: int) -> None:
        """Reduce health by the given amount, considering block/parry."""
        if self.parrying:
            return
        if self.blocking:
            amount //= 2
        self.health = max(0, self.health - amount)

    def use_mana(self, amount: int) -> bool:
        """Spend mana if available. Returns True if successful."""
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False

    def regen_mana(self, amount: int) -> None:
        """Regenerate mana up to max_mana."""
        self.mana = min(self.max_mana, self.mana + amount)

    def draw_status(self, surface: pygame.Surface, x: int = 10, y: int = 10) -> None:
        """Draw health and mana bars on the given surface."""
        bar_width = 100
        # Health bar (red)
        health_ratio = self.health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(x, y, bar_width, 10))
        pygame.draw.rect(
            surface,
            (0, 255, 0),
            pygame.Rect(x, y, int(bar_width * health_ratio), 10),
        )
        # Mana bar (blue)
        mana_ratio = self.mana / self.max_mana
        pygame.draw.rect(surface, (50, 50, 50), pygame.Rect(x, y + 15, bar_width, 10))
        pygame.draw.rect(
            surface,
            (0, 0, 255),
            pygame.Rect(x, y + 15, int(bar_width * mana_ratio), 10),
        )

    def set_gravity_multiplier(self, multiplier: float) -> None:
        """Adjust the gravity multiplier affecting this player."""
        self.gravity_multiplier = multiplier

    def update(self, ground_y: int, now: int | None = None) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        self.apply_gravity()
        self.pos += self.velocity
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        if self.parrying and now - self.last_parry >= PARRY_DURATION:
            self.parrying = False
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.pos.y = self.rect.top
            self.velocity.y = 0
            self.on_ground = True


class GuraPlayer(Player):
    """Player subclass implementing Gura's special trident attack."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import Projectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(20):
            self.last_special = now
            x = self.rect.centerx + self.direction * 25
            y = self.rect.centery
            proj = Projectile(x, y, self.direction)
            proj.image = pygame.Surface((15, 5))
            proj.image.fill((0, 255, 255))
            proj.velocity.x *= 1.5
            return proj
        return None


class Enemy(Player):
    """Basic enemy NPC using the same mechanics as players."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)

    def handle_ai(self, target: Player, now: int) -> None:
        """Very simple AI that follows the target."""
        if target.rect.centerx > self.rect.centerx:
            self.velocity.x = MOVE_SPEED / 2
            self.direction = 1
        else:
            self.velocity.x = -MOVE_SPEED / 2
            self.direction = -1
        if self.on_ground and abs(target.rect.centery - self.rect.centery) > 20:
            self.velocity.y = JUMP_VELOCITY
