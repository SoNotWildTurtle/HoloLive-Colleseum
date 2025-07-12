import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
from hololive_coliseum.player import PlayerCharacter, Enemy
from hololive_coliseum.projectile import Projectile
from hololive_coliseum.game import Game


def test_enemy_difficulty_reaction(monkeypatch):
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(100, 100)
    monkeypatch.setattr('random.random', lambda: 0.0)
    easy = Enemy(0, 100, difficulty="Easy")
    hard = Enemy(0, 100, difficulty="Hard")
    now = pygame.time.get_ticks()
    assert easy.handle_ai(player, now + 150, [], []) == (None, None)
    proj, melee = hard.handle_ai(player, now + 150, [], [])
    assert proj or melee
    proj2, melee2 = easy.handle_ai(player, now + 650, [], [])
    assert proj2 or melee2
    pygame.quit()


def test_enemy_projectile_hits_player(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    monkeypatch.setattr('random.random', lambda: 0.0)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.selected_character = "Gawr Gura"
    game.ai_players = 1
    game.difficulty_index = 2  # Hard
    game._setup_level()
    enemy = next(iter(game.enemies))
    enemy.last_ai_action = -1000
    now = pygame.time.get_ticks()
    proj, _ = enemy.handle_ai(game.player, now + 200, [], [])
    assert proj is not None
    proj.rect.center = game.player.rect.center
    game.projectiles.add(proj)
    game.all_sprites.add(proj)
    game._handle_collisions()
    assert game.player.health < game.player.max_health
    pygame.quit()


def test_enemy_dodges_projectile(monkeypatch):
    monkeypatch.setattr('random.random', lambda: 0.0)
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(100, 100)
    enemy = Enemy(50, 100, difficulty="Hard")
    proj = Projectile(55, 100, pygame.math.Vector2(-1, 0))
    projectiles = [proj]
    now = pygame.time.get_ticks() + 1000
    enemy.handle_ai(player, now, [], projectiles)
    assert enemy.dodging
    pygame.quit()
