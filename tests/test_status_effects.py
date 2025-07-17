import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
from hololive_coliseum.player import Enemy
from hololive_coliseum.status_effects import StatusEffectManager, FreezeEffect


def test_freeze_effect_expires():
    pygame.init()
    pygame.display.set_mode((1, 1))
    enemy = Enemy(0, 0)
    manager = StatusEffectManager()
    enemy.velocity.x = 4
    manager.add_effect(enemy, FreezeEffect(duration_ms=50))
    assert enemy.speed_factor == 0.5
    now = pygame.time.get_ticks() + 60
    manager.update(now)
    assert enemy.speed_factor == 1.0
    pygame.quit()
