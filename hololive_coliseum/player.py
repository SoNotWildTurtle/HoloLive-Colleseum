from __future__ import annotations
import os
import random
import pygame
from . import physics
JUMP_VELOCITY = -10
MOVE_SPEED = physics.MAX_MOVE_SPEED
import pygame

GRAVITY = 0.5
JUMP_VELOCITY = -10
MOVE_SPEED = 5
PROJECTILE_COOLDOWN = 250  # milliseconds
MELEE_COOLDOWN = 500  # milliseconds
PARRY_COOLDOWN = 1000  # milliseconds
PARRY_DURATION = 200  # milliseconds
SPECIAL_COOLDOWN = 1000  # milliseconds
DODGE_COOLDOWN = 800  # milliseconds
DODGE_DURATION = 200  # milliseconds
DODGE_SPEED = 8


class PlayerCharacter(pygame.sprite.Sprite):
    """Base controllable character sprite.

    Provides movement, combat mechanics and resource tracking. Subclasses
    override :py:meth:`special_attack` to implement unique abilities.
    """

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
        self.last_shot = -PROJECTILE_COOLDOWN
        self.last_melee = -MELEE_COOLDOWN
        self.last_parry = -PARRY_COOLDOWN
        self.parrying = False
        self.last_dodge = -DODGE_COOLDOWN
        self.dodging = False
        self.dodge_end = 0
        self.gravity_multiplier = 1.0
        self.friction_multiplier = 1.0
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
        self.lives = 3

        
    def handle_input(
        self,
        keys,
        now: int | None = None,
        key_bindings: dict[str, int] | None = None,
        action_pressed=None,
    ) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        if self.dodging:
            pass
        else:
            if keys[pygame.K_LEFT]:
                self.velocity.x = physics.accelerate(self.velocity.x, -1)
                self.direction = -1
            elif keys[pygame.K_RIGHT]:
                self.velocity.x = physics.accelerate(self.velocity.x, 1)
                self.direction = 1
            else:
                self.velocity.x = physics.apply_friction(
                    self.velocity.x, self.on_ground, self.friction_multiplier
                )
        
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
        if action_pressed is None:
            action_pressed = lambda act: keys[key_bindings.get(act, 0)]

        self.blocking = action_pressed("block")
        if action_pressed("parry"):
            self.parry(now)
        if action_pressed("dodge"):
            direction = (
                -1
                if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]
                else 1
                if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]
                else self.direction
            )
            self.dodge(now, direction)
        if self.on_ground and action_pressed("jump"):
            self.velocity.y = JUMP_VELOCITY
            self.on_ground = False

    def shoot(self, now: int, target: tuple[int, int] | None = None):
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
            x = self.rect.centerx
            y = self.rect.centery
            if target:
                direction = pygame.math.Vector2(target[0] - x, target[1] - y)
            else:
                direction = pygame.math.Vector2(self.direction, 0)
            return Projectile(x, y, direction)
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

    def dodge(self, now: int, direction: int) -> bool:
        """Perform a quick dodge movement if cooldown allows."""
        if now - self.last_dodge >= DODGE_COOLDOWN:
            self.last_dodge = now
            self.dodging = True
            self.dodge_end = now + DODGE_DURATION
            self.velocity.x = DODGE_SPEED * direction
            return True
        return False

    def apply_gravity(self) -> None:
        self.velocity.y = physics.apply_gravity(self.velocity.y, self.gravity_multiplier)
    def apply_gravity(self) -> None:
        self.velocity.y += GRAVITY * self.gravity_multiplier

    def take_damage(self, amount: int) -> None:
        """Reduce health by the given amount, considering block/parry."""
        if self.parrying:
            return
        if self.blocking:
            amount //= 2
        self.health = max(0, self.health - amount)
        if self.health == 0 and self.lives > 0:
            self.lives -= 1
            self.health = self.max_health

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
        lives_text = pygame.font.SysFont(None, 24).render(
            f"Lives: {self.lives}", True, (255, 255, 255)
        )
        surface.blit(lives_text, (x, y + 30))

    def set_gravity_multiplier(self, multiplier: float) -> None:
        """Adjust the gravity multiplier affecting this player."""
        self.gravity_multiplier = multiplier

    def set_friction_multiplier(self, multiplier: float) -> None:
        """Adjust horizontal friction when on special surfaces."""
        self.friction_multiplier = multiplier

    def update(self, ground_y: int, now: int | None = None) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        self.apply_gravity()
        self.pos += self.velocity
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        if self.dodging and now >= self.dodge_end:
            self.dodging = False
        if self.parrying and now - self.last_parry >= PARRY_DURATION:
            self.parrying = False
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.pos.y = self.rect.top
            self.velocity.y = 0
            self.on_ground = True


class GuraPlayer(PlayerCharacter):
class GuraPlayer(Player):
    """Player subclass implementing Gura's special trident attack."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import ExplodingProjectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(20):
            self.last_special = now
            x = self.rect.centerx
            y = self.rect.centery
            direction = pygame.math.Vector2(self.direction, 0)
            proj = ExplodingProjectile(x, y, direction)
            proj.image = pygame.Surface((15, 5))
            proj.image.fill((0, 255, 255))
            proj.velocity *= 1.5
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


class WatsonPlayer(PlayerCharacter):
    """Watson Amelia with a time-dash special attack."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN
        self.dashing = False
        self.dash_end = 0

    def special_attack(self, now: int):
        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(15):
            self.last_special = now
            self.dashing = True
            self.dash_end = now + 300
            self.velocity.x = 15 * self.direction
        return None

    def update(self, ground_y: int, now: int | None = None) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        if self.dashing and now >= self.dash_end:
            self.dashing = False
        super().update(ground_y, now)


class InaPlayer(PlayerCharacter):
    """Ninomae Ina'nis with a tentacle grapple special attack."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import GrappleProjectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(15):
            self.last_special = now
            x = self.rect.centerx
            y = self.rect.centery
            direction = pygame.math.Vector2(self.direction, 0)
            proj = GrappleProjectile(x, y, direction)
            proj.image.fill((128, 0, 255))
            return proj
        return None


class KiaraPlayer(PlayerCharacter):
    """Takanashi Kiara's fiery leap that explodes on landing."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN
        self.diving = False

    def special_attack(self, now: int):
        if not self.diving and now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(20):
            self.last_special = now
            self.velocity.y = JUMP_VELOCITY * 1.5
            self.diving = True
        return None

    def update(self, ground_y: int, now: int | None = None) -> None:
        super().update(ground_y, now)
        if self.diving and self.on_ground:
            self.diving = False
            from .projectile import ExplosionProjectile
            return ExplosionProjectile(self.rect.centerx, self.rect.bottom - 10)
        return None


class CalliopePlayer(PlayerCharacter):
    """Mori Calliope's returning scythe projectile."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import BoomerangProjectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(20):
            self.last_special = now
            return BoomerangProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
                self,
            )
        return None


class FaunaPlayer(PlayerCharacter):
    """Ceres Fauna creates a healing field to restore health."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .healing_zone import HealingZone

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(15):
            self.last_special = now
            zone_rect = self.rect.inflate(80, 40)
            zone_rect.center = self.rect.center
            return HealingZone(zone_rect)
        return None


class KroniiPlayer(PlayerCharacter):
    """Ouro Kronii parry lasts longer as a special."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(15):
            self.last_special = now
            self.parry(now)
            self.last_parry -= 300  # extend duration
        return None


class IRySPlayer(PlayerCharacter):
    """IRyS deploys a shield that blocks projectiles."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN
        self.shield_active = False
        self.shield_end = 0

    def special_attack(self, now: int):
        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(15):
            self.last_special = now
            self.shield_active = True
            self.shield_end = now + 1000
        return None

    def update(self, ground_y: int, now: int | None = None) -> None:
        super().update(ground_y, now)
        if self.shield_active and now is not None and now >= self.shield_end:
            self.shield_active = False


class MumeiPlayer(PlayerCharacter):
    """Nanashi Mumei summons a slowing flock."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import FlockProjectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(15):
            self.last_special = now
            return FlockProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
        return None


class BaelzPlayer(PlayerCharacter):
    """Hakos Baelz triggers random chaos effects."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(20):
            self.last_special = now
            effect = random.choice(["invert", "low_gravity"])
            if effect == "invert":
                self.direction *= -1
            else:
                self.set_gravity_multiplier(0.5)
        return None


class FubukiPlayer(PlayerCharacter):
    """Shirakami Fubuki fires an ice shard that slows enemies."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import FreezingProjectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(15):
            self.last_special = now
            return FreezingProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
        return None


class MikoPlayer(PlayerCharacter):
    """Sakura Miko fires a piercing beam that passes through enemies."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import PiercingProjectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(20):
            self.last_special = now
            return PiercingProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
        return None


class AquaPlayer(PlayerCharacter):
    """Minato Aqua fires a water blast that explodes."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import ExplodingProjectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(20):
            self.last_special = now
            proj = ExplodingProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            proj.image.fill((0, 100, 255))
            return proj
        return None


class PekoraPlayer(PlayerCharacter):
    """Usada Pekora tosses an explosive carrot."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import ExplodingProjectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(20):
            self.last_special = now
            proj = ExplodingProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            proj.image.fill((255, 165, 0))
            return proj
        return None


class MarinePlayer(PlayerCharacter):
    """Houshou Marine's anchor boomerang."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import BoomerangProjectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(20):
            self.last_special = now
            proj = BoomerangProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
                self,
            )
            proj.image.fill((255, 0, 128))
            return proj
        return None


class SuiseiPlayer(PlayerCharacter):
    """Hoshimachi Suisei shoots a piercing star."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import PiercingProjectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(20):
            self.last_special = now
            proj = PiercingProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            proj.image.fill((100, 200, 255))
            return proj
        return None


class AyamePlayer(PlayerCharacter):
    """Nakiri Ayame performs a swift dash."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN
        self.dashing = False
        self.dash_end = 0

    def special_attack(self, now: int):
        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(15):
            self.last_special = now
            self.dashing = True
            self.dash_end = now + 300
            self.velocity.x = 15 * self.direction
        return None

    def update(self, ground_y: int, now: int | None = None) -> None:
        if now is None:
            now = pygame.time.get_ticks()
        if self.dashing and now >= self.dash_end:
            self.dashing = False
        super().update(ground_y, now)


class NoelPlayer(PlayerCharacter):
    """Shirogane Noel smashes the ground causing an explosion."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import ExplosionProjectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(20):
            self.last_special = now
            return ExplosionProjectile(
                self.rect.centerx,
                self.rect.bottom - 10,
            )
        return None


class FlarePlayer(PlayerCharacter):
    """Shiranui Flare fires a burst of flames."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import ExplodingProjectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(20):
            self.last_special = now
            proj = ExplodingProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            proj.image.fill((255, 80, 0))
            return proj
        return None


class SubaruPlayer(PlayerCharacter):
    """Oozora Subaru launches a stunning blast."""

    def __init__(self, x: int, y: int, image_path: str | None = None) -> None:
        super().__init__(x, y, image_path)
        self.last_special = -SPECIAL_COOLDOWN

    def special_attack(self, now: int):
        from .projectile import ExplodingProjectile

        if now - self.last_special >= SPECIAL_COOLDOWN and self.use_mana(20):
            self.last_special = now
            proj = ExplodingProjectile(
                self.rect.centerx,
                self.rect.centery,
                pygame.math.Vector2(self.direction, 0),
            )
            proj.image.fill((255, 255, 0))
            return proj
        return None


class Enemy(PlayerCharacter):
    """AI controlled opponent sharing the player mechanics."""

    AI_LEVELS = {
        "Easy": {
            "react_ms": 600,
            "speed": 0.6,
            "shoot_prob": 1.0,
            "melee_prob": 1.0,
            "jump_prob": 0.1,
            "dodge_prob": 0.2,
        },
        "Normal": {
            "react_ms": 300,
            "speed": 0.8,
            "shoot_prob": 1.0,
            "melee_prob": 1.0,
            "jump_prob": 0.2,
            "dodge_prob": 0.4,
        },
        "Hard": {
            "react_ms": 100,
            "speed": 1.0,
            "shoot_prob": 1.0,
            "melee_prob": 1.0,
            "jump_prob": 0.4,
            "dodge_prob": 0.6,
        },
    }

    def __init__(
        self,
        x: int,
        y: int,
        image_path: str | None = None,
        difficulty: str = "Normal",
    ) -> None:
        super().__init__(x, y, image_path)
        self.difficulty = difficulty
        self.last_ai_action = 0
        self.lives = 1

    def take_damage(self, amount: int) -> None:
        if self.blocking:
            amount //= 2
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.kill()

    def shoot(self, now: int, target: tuple[int, int] | None = None):
        proj = super().shoot(now, target)
        if proj:
            proj.from_enemy = True
        return proj

    def melee_attack(self, now: int):
        attack = super().melee_attack(now)
        if attack:
            attack.from_enemy = True
        return attack

    def handle_ai(
        self,
        target: PlayerCharacter,
        now: int,
        hazards=None,
        projectiles=None,
    ):
        """React to the player based on difficulty level."""
        settings = self.AI_LEVELS.get(self.difficulty, self.AI_LEVELS["Normal"])
        hazards = hazards or []
        projectiles = projectiles or []
        if now - self.last_ai_action < settings["react_ms"]:
            return None, None
        self.last_ai_action = now
        for p in projectiles:
            if p.rect.colliderect(self.rect.inflate(30, 30)) and random.random() < settings["dodge_prob"]:
                self.dodge(now, -self.direction)
                return None, None
        for hz in hazards:
            if getattr(hz, "avoid", False) and hz.rect.colliderect(
                self.rect.move(self.direction * 5, 0)
            ):
                if self.on_ground:
                    self.velocity.y = JUMP_VELOCITY
                break
        if target.rect.centerx > self.rect.centerx:
            self.velocity.x = physics.accelerate(self.velocity.x, 1) * settings[
                "speed"
            ]
            self.direction = 1
        else:
            self.velocity.x = physics.accelerate(self.velocity.x, -1) * settings[
                "speed"
            ]
            self.direction = -1
        if (
            self.on_ground
            and abs(target.rect.centery - self.rect.centery) > 20
            and random.random() < settings["jump_prob"]
        ):
            self.velocity.y = JUMP_VELOCITY
        dist_x = abs(target.rect.centerx - self.rect.centerx)
        melee = None
        proj = None
        if self.difficulty == "Hard":
            if dist_x < 40:
                melee = self.melee_attack(now)
            elif dist_x < 250:
                proj = self.shoot(now, target.rect.center)
        else:
            if dist_x < 40 and (
                settings["melee_prob"] >= 1 or random.random() < settings["melee_prob"]
            ):
                melee = self.melee_attack(now)
            elif dist_x < 250 and (
                settings["shoot_prob"] >= 1 or random.random() < settings["shoot_prob"]
            ):
                proj = self.shoot(now, target.rect.center)
        return proj, melee

# Alias for backward compatibility
Player = PlayerCharacter

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
