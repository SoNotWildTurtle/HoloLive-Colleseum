import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def test_game_initialization():
    from hololive_coliseum.game import Game
    game = Game()
    assert game.width == 800
    assert game.height == 600
