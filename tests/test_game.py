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
