import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
from hololive_coliseum.player import PlayerCharacter, Enemy
from hololive_coliseum.ai_manager import AIManager
from hololive_coliseum.npc_manager import NPCManager
from hololive_coliseum.ally_manager import AllyManager


def test_ai_manager_actions(monkeypatch):
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(100, 100)
    enemy = Enemy(0, 100, difficulty="Hard")
    enemy.last_ai_action = -1000
    mgr = AIManager(pygame.sprite.Group(enemy))
    monkeypatch.setattr('random.random', lambda: 0.0)
    projs, melees = mgr.update(player, pygame.time.get_ticks(), [], [])
    assert projs or melees
    pygame.quit()


def test_npc_and_ally_manager_groups():
    mgr = NPCManager()
    ally_mgr = AllyManager(mgr.allies)
    p1 = PlayerCharacter(0, 0)
    p2 = PlayerCharacter(0, 0)
    mgr.add_enemy(p1)
    mgr.add_ally(p2)
    assert p1 in mgr.enemies
    assert p2 in mgr.allies
    ally_mgr.update(p1, 100, 0)
