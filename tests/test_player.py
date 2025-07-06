import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame

from hololive_coliseum.player import Player


def test_player_gravity():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = Player(0, 0)
    player.update(ground_y=1000)
    assert player.velocity.y > 0
    pygame.quit()


def test_player_friction_slows_movement():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = Player(0, 0)
    player.velocity.x = 3
    player.on_ground = True
    dummy_keys = type('D', (), {'__getitem__': lambda self, key: False})()
    player.handle_input(dummy_keys, pygame.time.get_ticks(), action_pressed=lambda a: False)
    player.update(ground_y=1000)
    assert player.velocity.x < 3
    pygame.quit()


def test_player_loads_image():
    pygame.init()
    pygame.display.set_mode((1, 1))
    image_path = os.path.join(
        os.path.dirname(__file__), "..", "Images", "Gawr_Gura_right.png"
    )
    player = Player(0, 0, image_path)
    assert player.image.get_size() == (64, 64)
    pygame.quit()


def test_player_health_mana_usage():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = Player(0, 0)
    player.take_damage(30)
    assert player.health == 70
    assert player.use_mana(20)
    assert player.mana == 80
    assert not player.use_mana(100)
    pygame.quit()


def test_draw_status_updates_surface():
    pygame.init()
    screen = pygame.display.set_mode((120, 50))
    player = Player(0, 0)
    player.health = 50
    player.mana = 25
    player.draw_status(screen)
    # Check a pixel within the health bar is green when half health
    assert screen.get_at((15, 10))[:3] == (0, 255, 0)
    # Mana bar should have blue pixel when quarter mana
    assert screen.get_at((15, 25))[:3] == (0, 0, 255)
    pygame.quit()


def test_melee_attack_and_block():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = Player(0, 0)
    now = pygame.time.get_ticks()
    attack = player.melee_attack(now)
    assert attack is not None
    # Cooldown prevents immediate second attack
    assert player.melee_attack(now) is None
    player.blocking = True
    player.health = 100
    player.take_damage(20)
    assert player.health == 90  # half damage when blocking
    pygame.quit()


def test_parry_prevents_damage():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = Player(0, 0)
    now = pygame.time.get_ticks()
    assert player.parry(now)
    player.take_damage(50)
    assert player.health == player.max_health
    player.update(1000, now + 300)
    player.take_damage(50)
    assert player.health == player.max_health - 50
    pygame.quit()


def test_gura_special_attack():
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.player import GuraPlayer

    player = GuraPlayer(0, 0)
    now = pygame.time.get_ticks()
    proj = player.special_attack(now)
    assert proj is not None
    assert player.mana < player.max_mana
    assert player.special_attack(now) is None  # cooldown active
    pygame.quit()


def test_watson_special_dash():
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.player import WatsonPlayer

    player = WatsonPlayer(0, 0)
    now = pygame.time.get_ticks()
    player.velocity.x = 0
    player.special_attack(now)
    assert player.velocity.x != 0
    assert player.mana < player.max_mana
    pygame.quit()


def test_player_lives_decrease():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = Player(0, 0)
    player.take_damage(200)
    assert player.lives == 2
    pygame.quit()
