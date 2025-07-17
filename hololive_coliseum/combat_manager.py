"""Combat related helpers."""

import pygame

from .damage_manager import DamageManager
from .status_effects import StatusEffectManager, FreezeEffect, SlowEffect


class CombatManager:
    """Manage combat turns and collision handling."""

    def __init__(self, status_manager: StatusEffectManager | None = None) -> None:
        self.participants: list = []
        self.index = 0
        self.status_manager = status_manager or StatusEffectManager()
        self.damage_manager = DamageManager()
        self.last_enemy_damage = 0

    def add(self, actor) -> None:
        """Add a combatant to the turn list."""
        self.participants.append(actor)

    def remove(self, actor) -> None:
        if actor in self.participants:
            self.participants.remove(actor)

    def next_actor(self):
        """Return the next actor in the turn order."""
        if not self.participants:
            return None
        actor = self.participants[self.index % len(self.participants)]
        self.index += 1
        return actor

    def handle_collisions(
        self,
        player,
        enemies,
        projectiles,
        melee_attacks,
        now: int,
    ) -> int:
        """Process projectile and melee collisions.

        Returns the number of enemies killed so the caller can update score.
        """
        kills = 0
        for proj in list(projectiles):
            if getattr(proj, "from_enemy", False):
                if player.rect.colliderect(proj.rect):
                    if getattr(player, "shield_active", False):
                        proj.kill()
                    else:
                        player.take_damage(10)
                        proj.kill()
                continue
            hits = pygame.sprite.spritecollide(proj, enemies, False)
            if hits:
                for enemy in hits:
                    if getattr(proj, "grapple", False):
                        enemy.rect.centerx = player.rect.centerx
                        enemy.pos.x = enemy.rect.x
                    elif getattr(proj, "freeze", False):
                        self.status_manager.add_effect(enemy, FreezeEffect())
                        enemy.take_damage(5)
                    elif getattr(proj, "slow", False):
                        self.status_manager.add_effect(enemy, SlowEffect())
                        enemy.take_damage(5)
                    else:
                        enemy.take_damage(10)
                    if enemy.health == 0:
                        enemy.kill()
                        kills += 1
                if not getattr(proj, "pierce", False):
                    proj.kill()
        for attack in list(melee_attacks):
            if getattr(attack, "from_enemy", False):
                if attack.rect.colliderect(player.rect):
                    player.take_damage(15)
                attack.kill()
                continue
            hits = pygame.sprite.spritecollide(attack, enemies, False)
            if hits:
                for enemy in hits:
                    enemy.take_damage(15)
                    if enemy.health == 0:
                        enemy.kill()
                        kills += 1
            attack.kill()
        if (
            pygame.sprite.spritecollideany(player, enemies)
            and now - self.last_enemy_damage >= 500
        ):
            player.take_damage(10)
            self.last_enemy_damage = now
        return kills

    def add(self, actor) -> None:
        """Add a combatant to the turn list."""
        self.participants.append(actor)

    def remove(self, actor) -> None:
        if actor in self.participants:
            self.participants.remove(actor)

    def next_actor(self):
        """Return the next actor in the turn order."""
        if not self.participants:
            return None
        actor = self.participants[self.index % len(self.participants)]
        self.index += 1
        return actor
