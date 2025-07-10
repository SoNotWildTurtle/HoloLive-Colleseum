import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def test_game_initialization(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    from hololive_coliseum.game import Game
    game = Game()
    assert game.width == 800
    assert game.height == 600


def test_draw_menu_fills_cyan(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR
    game = Game(width=100, height=100)
    game._draw_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_game_has_mp_type_menu(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    from hololive_coliseum.game import Game
    game = Game()
    assert game.mp_type_options == ["Offline", "Online"]


def test_draw_key_bindings_menu(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR
    game = Game(width=120, height=90)
    game._draw_key_bindings_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_controller_menu_options(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    from hololive_coliseum.game import Game
    game = Game()
    assert "Controller Bindings" in game.settings_options


def test_character_menu_has_ai_option(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    from hololive_coliseum.game import Game
    game = Game()
    assert "Add AI Player" in game.character_menu_options


def test_watson_in_character_list(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    from hololive_coliseum.game import Game
    game = Game()
    assert "Watson Amelia" in game.characters


def test_ina_in_character_list(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    from hololive_coliseum.game import Game
    game = Game()
    assert "Ninomae Ina'nis" in game.characters


def test_ai_players_spawn(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    from hololive_coliseum.game import Game
    game = Game()
    game.selected_character = "Gawr Gura"
    game.ai_players = 2
    game._setup_level()
    assert len(game.enemies) == 2


def test_setup_level_resets_timers(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    from hololive_coliseum.game import Game
    game = Game()
    game.next_powerup_time = 123
    game.last_enemy_damage = 456
    game.ai_players = 0
    game._setup_level()
    assert game.next_powerup_time == 0
    assert game.last_enemy_damage == 0


def test_enemy_ai_moves_toward_player(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    from hololive_coliseum.game import Game
    import pygame
    game = Game()
    game.ai_players = 1
    game._setup_level()
    game.last_enemy_damage = -1000
    enemy = next(iter(game.enemies))
    start_x = enemy.rect.x
    now = pygame.time.get_ticks()
    enemy.handle_ai(game.player, now)
    enemy.update(game.ground_y, now)
    assert enemy.rect.x != start_x


def test_enemy_collision_hurts_player(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.ai_players = 1
    game._setup_level()
    game.last_enemy_damage = -1000
    enemy = next(iter(game.enemies))
    enemy.rect.center = game.player.rect.center
    enemy.pos = pygame.math.Vector2(enemy.rect.topleft)
    game._handle_collisions()
    assert game.player.health < game.player.max_health
    pygame.quit()


def test_chapter_list_has_20_entries(tmp_path, monkeypatch):
    monkeypatch.setattr('hololive_coliseum.save_manager.SAVE_DIR', tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert len(game.chapters) == 20
    assert len(game.chapter_images) == 20
