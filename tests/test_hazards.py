import os
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame

from hololive_coliseum.hazards import SpikeTrap, IceZone
from hololive_coliseum.game import Game
from hololive_coliseum.player import Enemy


def test_spike_trap_damages_player(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    trap = SpikeTrap(game.player.rect.copy())
    game.hazards.add(trap)
    game.all_sprites.add(trap)
    now = pygame.time.get_ticks()
    game.last_hazard_damage = -1000
    game.state = 'playing'
    game._handle_collisions()  # to avoid unused
    zone = pygame.sprite.spritecollideany(game.player, game.hazards)
    if zone:
        game.player.take_damage(trap.damage)
    assert game.player.health < game.player.max_health
    pygame.quit()


def test_enemy_jumps_over_hazard(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    game = Game()
    game.ai_players = 1
    game._setup_level()
    enemy = next(iter(game.enemies))
    trap_rect = enemy.rect.move(5, 0)
    trap = SpikeTrap(trap_rect)
    game.hazards.add(trap)
    enemy.on_ground = True
    now = pygame.time.get_ticks() + 1000
    enemy.handle_ai(game.player, now, game.hazards, [])
    assert enemy.velocity.y == -10
    pygame.quit()

