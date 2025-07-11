import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame

from hololive_coliseum.player import PlayerCharacter


def test_player_gravity():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    player.update(ground_y=1000)
    assert player.velocity.y > 0
    pygame.quit()


def test_player_friction_slows_movement():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
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
    player = PlayerCharacter(0, 0, image_path)
    assert player.image.get_size() == (64, 64)
    pygame.quit()


def test_player_health_mana_usage():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    player.take_damage(30)
    assert player.health == 70
    assert player.use_mana(20)
    assert player.mana == 80
    assert not player.use_mana(100)
    pygame.quit()


def test_draw_status_updates_surface():
    pygame.init()
    screen = pygame.display.set_mode((120, 50))
    player = PlayerCharacter(0, 0)
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
    player = PlayerCharacter(0, 0)
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
    player = PlayerCharacter(0, 0)
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


def test_ina_grapple_projectile(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Ninomae Ina'nis"
    game.ai_players = 1
    game._setup_level()
    enemy = next(iter(game.enemies))
    now = pygame.time.get_ticks()
    proj = game.player.special_attack(now)
    assert proj is not None
    proj.rect.center = enemy.rect.center
    game.projectiles.add(proj)
    game.all_sprites.add(proj)
    game._handle_collisions()
    assert enemy.rect.centerx == game.player.rect.centerx
    pygame.quit()


def test_player_lives_decrease():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    player.take_damage(200)
    assert player.lives == 2
    pygame.quit()


def test_fubuki_freeze_special():
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.player import FubukiPlayer, Enemy
    from hololive_coliseum.projectile import FreezingProjectile
    from hololive_coliseum.game import Game

    game = Game()
    player = FubukiPlayer(0, 0)
    enemy = Enemy(60, 0)
    enemy.velocity.x = 2
    game.player = player
    game.enemies = pygame.sprite.Group(enemy)
    proj = player.special_attack(pygame.time.get_ticks())
    assert isinstance(proj, FreezingProjectile)
    proj.rect.center = enemy.rect.center
    game.projectiles = pygame.sprite.Group(proj)
    game.melee_attacks = pygame.sprite.Group()
    game.all_sprites = pygame.sprite.Group(player, enemy, proj)
    game._handle_collisions()
    assert enemy.velocity.x == 1
    assert enemy.health == enemy.max_health - 5
    pygame.quit()


def test_mumei_flock_special():
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.player import MumeiPlayer, Enemy
    from hololive_coliseum.projectile import FlockProjectile
    from hololive_coliseum.game import Game

    player = MumeiPlayer(0, 0)
    enemy = Enemy(60, 0)
    enemy.velocity.x = 2
    game = Game()
    game.player = player
    proj = player.special_attack(pygame.time.get_ticks())
    assert isinstance(proj, FlockProjectile)
    proj.rect.center = enemy.rect.center
    game.enemies = pygame.sprite.Group(enemy)
    game.projectiles = pygame.sprite.Group(proj)
    game.melee_attacks = pygame.sprite.Group()
    game.all_sprites = pygame.sprite.Group(player, enemy, proj)
    game._handle_collisions()
    assert enemy.velocity.x == 1
    assert enemy.health == enemy.max_health - 5
    pygame.quit()


def test_fauna_healing_zone():
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.player import FaunaPlayer
    from hololive_coliseum.healing_zone import HealingZone

    player = FaunaPlayer(0, 0)
    player.health = 50
    zone = player.special_attack(pygame.time.get_ticks())
    assert isinstance(zone, HealingZone)
    # Player stands in the zone and should heal
    if zone.rect.colliderect(player.rect):
        player.health = min(player.max_health, player.health + zone.heal_rate)
    assert player.health > 50
    pygame.quit()


def test_player_dodge():
    pygame.init()
    pygame.display.set_mode((1, 1))
    player = PlayerCharacter(0, 0)
    now = pygame.time.get_ticks()
    assert player.dodge(now, 1)
    assert player.dodging
    player.update(1000, now + 300)
    assert not player.dodging
    pygame.quit()


def test_calliope_boomerang_projectile():
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.player import CalliopePlayer
    from hololive_coliseum.projectile import BoomerangProjectile

    player = CalliopePlayer(0, 0)
    now = pygame.time.get_ticks()
    proj = player.special_attack(now)
    assert isinstance(proj, BoomerangProjectile)
    right_vel = proj.velocity.x
    for _ in range(16):
        proj.update()
    assert proj.velocity.x != right_vel
    assert proj.velocity.x < 0  # now returning toward player
    pygame.quit()


def test_kiara_dive_explosion(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game
    from hololive_coliseum.player import KiaraPlayer, Enemy

    game = Game()
    game.player = KiaraPlayer(0, game.ground_y - 60)
    enemy = Enemy(10, game.ground_y - 60)
    game.enemies = pygame.sprite.Group(enemy)
    game.projectiles = pygame.sprite.Group()
    game.melee_attacks = pygame.sprite.Group()
    game.all_sprites = pygame.sprite.Group(game.player, enemy)
    now = pygame.time.get_ticks()
    game.player.special_attack(now)
    extra = None
    for i in range(80):
        extra = game.player.update(game.ground_y, now + 50 * i)
        if extra:
            game.projectiles.add(extra)
            game.all_sprites.add(extra)
            break
    game.projectiles.update()
    game._handle_collisions()
    assert enemy.health < enemy.max_health
    pygame.quit()


def test_irys_shield_blocks_projectile(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game
    from hololive_coliseum.player import IRySPlayer, Enemy
    from hololive_coliseum.projectile import Projectile

    game = Game()
    game.player = IRySPlayer(0, 0)
    enemy = Enemy(60, 0)
    proj = Projectile(game.player.rect.centerx, game.player.rect.centery, pygame.math.Vector2(0, 0), True)
    game.enemies = pygame.sprite.Group(enemy)
    game.projectiles = pygame.sprite.Group(proj)
    game.melee_attacks = pygame.sprite.Group()
    game.all_sprites = pygame.sprite.Group(game.player, proj)
    game.player.special_attack(pygame.time.get_ticks())
    health = game.player.health
    game._handle_collisions()
    assert game.player.health == health
    assert not proj.alive()
    pygame.quit()


def test_miko_piercing_beam():
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.player import MikoPlayer, Enemy
    from hololive_coliseum.projectile import PiercingProjectile
    from hololive_coliseum.game import Game

    player = MikoPlayer(0, 0)
    enemy = Enemy(60, 0)
    game = Game()
    game.player = player
    game.enemies = pygame.sprite.Group(enemy)
    proj = player.special_attack(pygame.time.get_ticks())
    assert isinstance(proj, PiercingProjectile)
    proj.rect.center = enemy.rect.center
    game.projectiles = pygame.sprite.Group(proj)
    game.melee_attacks = pygame.sprite.Group()
    game.all_sprites = pygame.sprite.Group(player, enemy, proj)
    game._handle_collisions()
    assert proj.alive()  # piercing projectile remains
    assert enemy.health == enemy.max_health - 10
    pygame.quit()
