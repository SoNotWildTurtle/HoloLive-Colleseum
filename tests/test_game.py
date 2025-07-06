import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def test_game_initialization():
    from hololive_coliseum.game import Game
    game = Game()
    assert game.width == 800
    assert game.height == 600


def test_draw_menu_fills_cyan():
    from hololive_coliseum.game import Game, MENU_BG_COLOR
    game = Game(width=100, height=100)
    game._draw_menu()
    assert game.screen.get_at((0, 0))[:3] == MENU_BG_COLOR
