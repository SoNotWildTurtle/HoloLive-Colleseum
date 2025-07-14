import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def test_game_initialization(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert game.width == 800
    assert game.height == 600


def test_draw_menu_fills_cyan(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=100, height=100)
    game._draw_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_game_has_mp_type_menu(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert game.mp_type_options == ["Offline", "Online", "Back"]


def test_draw_key_bindings_menu(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=120, height=90)
    game._draw_key_bindings_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_controller_menu_options(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "Controller Bindings" in game.settings_options


def test_character_menu_has_ai_option(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "Add AI Player" in game.character_menu_options


def test_character_menu_has_difficulty(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "Difficulty" in game.character_menu_options
    assert game.difficulty_levels == ["Easy", "Normal", "Hard"]


def test_watson_in_character_list(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "Watson Amelia" in game.characters


def test_ina_in_character_list(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "Ninomae Ina'nis" in game.characters


def test_fubuki_in_character_list(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "Shirakami Fubuki" in game.characters


def test_character_list_has_20_entries(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert len(game.characters) == 21
    assert "Tokino Sora" in game.characters


def test_ai_players_spawn(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Gawr Gura"
    game.ai_players = 2
    game._setup_level()
    assert len(game.enemies) == 2


def test_setup_level_resets_timers(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game.next_powerup_time = 123
    game.last_enemy_damage = 456
    game.ai_players = 0
    game._setup_level()
    assert game.next_powerup_time == 0
    assert game.last_enemy_damage == 0


def test_setup_level_adds_two_gravity_zones(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game.ai_players = 0
    game._setup_level()
    assert len(game.gravity_zones) == 2
    multipliers = sorted(zone.multiplier for zone in game.gravity_zones)
    assert multipliers == [0.2, 2.0]


def test_enemy_ai_moves_toward_player(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game
    import pygame

    game = Game()
    game.ai_players = 1
    game._setup_level()
    game.last_enemy_damage = -1000
    enemy = next(iter(game.enemies))
    start_x = enemy.rect.x
    now = pygame.time.get_ticks()
    enemy.handle_ai(game.player, now, [], [])
    enemy.update(game.ground_y, now)
    assert enemy.rect.x != start_x


def test_enemy_collision_hurts_player(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
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
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert len(game.chapters) == 20
    assert len(game.chapter_images) == 20


def test_map_menu_has_back_option(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert game.map_menu_options[-1] == "Back"


def test_character_menu_has_back_option(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert game.character_menu_options[-1] == "Back"


def test_pause_menu_options(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert game.pause_options == ["Resume", "Main Menu"]


def test_draw_pause_menu(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=90, height=90)
    game._draw_pause_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_main_menu_has_info_options(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "How to Play" in game.main_menu_options
    assert "Credits" in game.main_menu_options
    assert "Records" in game.main_menu_options


def test_draw_how_to_play(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=80, height=80)
    game._draw_how_to_play()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_draw_credits(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=80, height=80)
    game._draw_credits()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_draw_scoreboard(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=80, height=80)
    game._draw_scoreboard_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_escape_enters_pause(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame
    from hololive_coliseum.game import Game

    game = Game()
    game.state = "playing"
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert game.state == "paused"


def test_draw_lobby_menu(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game, MENU_BG_COLOR

    game = Game(width=100, height=100)
    game.player_names = ["P1", "P2"]
    game._draw_lobby_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR


def test_cycle_volume(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game.volume = 0.0
    game._cycle_volume()
    assert game.volume == 0.5
    game._cycle_volume()
    assert game.volume == 1.0
    game._cycle_volume()
    assert game.volume == 0.0


def test_node_settings_menu(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "Node Settings" in game.settings_options
    assert game.node_options == ["Start Node", "Stop Node", "Latency Helper", "Back"]


def test_accounts_menu(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "Accounts" in game.settings_options
    assert game.account_options == ["Register Account", "Delete Account", "Back"]


def test_settings_menu_has_new_options(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert "Show FPS" in game.settings_options
    assert "Reset Records" in game.settings_options


def test_start_and_stop_node(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    game.start_node()
    assert game.network_manager is not None
    assert game.node_hosting
    game.stop_node()
    assert game.network_manager is None
    assert not game.node_hosting


def test_game_over_state(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    game.player.lives = 0
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert game.state == "game_over"
    pygame.quit()


def test_best_time_saved(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game, load_settings

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    game.level_start_time = pygame.time.get_ticks() - 3000
    game.player.lives = 0
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    settings = load_settings()
    assert settings.get("best_time", 0) >= 3
    pygame.quit()


def test_best_score_saved(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game, load_settings

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    game.score = 5
    game.player.lives = 0
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    settings = load_settings()
    assert settings.get("best_score", 0) >= 5
    pygame.quit()


def test_enemy_kill_increments_score(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game
    from hololive_coliseum.projectile import Projectile

    game = Game()
    game.selected_character = "Gawr Gura"
    game.ai_players = 1
    game._setup_level()
    enemy = next(iter(game.enemies))
    enemy.health = 5
    proj = Projectile(enemy.rect.centerx, enemy.rect.centery, pygame.math.Vector2(1, 0))
    game.projectiles.add(proj)
    game._handle_collisions()
    assert game.score == 1
    assert len(game.enemies) == 0
    pygame.quit()


def test_victory_state(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    game.level_start_time = pygame.time.get_ticks() - game.level_limit * 1000 - 100
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert game.state == "victory"
    pygame.quit()


def test_final_time_victory(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    game.level_start_time = pygame.time.get_ticks() - game.level_limit * 1000 - 100
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert game.final_time >= game.level_limit
    pygame.quit()


def test_final_time_game_over(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    game.level_start_time = pygame.time.get_ticks() - 2000
    game.player.lives = 0
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert game.final_time >= 2
    pygame.quit()


def test_end_menu_options(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    from hololive_coliseum.game import Game

    game = Game()
    assert game.game_over_options == ["Play Again", "Main Menu"]
    assert game.victory_options == ["Play Again", "Main Menu"]


def test_play_again_returns_to_char(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.state = "victory"
    game.show_end_options = True
    game.menu_index = 0  # Play Again
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert game.state == "char"
    pygame.quit()


def test_chat_toggle_and_send(tmp_path, monkeypatch):
    monkeypatch.setattr("hololive_coliseum.save_manager.SAVE_DIR", tmp_path)
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    from hololive_coliseum.game import Game

    game = Game()
    game.selected_character = "Gawr Gura"
    game._setup_level()
    game.state = "playing"
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": "\r"}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_h, "unicode": "h"}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_i, "unicode": "i"}))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "unicode": "\r"}))
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.run()
    assert not game.chat_manager.open
    assert game.chat_manager.history() == [("Player 1", "hi")]
    pygame.quit()
