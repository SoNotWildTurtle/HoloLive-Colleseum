import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from hololive_coliseum.player import Player


def test_player_gravity():
    player = Player(0, 0)
    player.update(ground_y=1000)
    assert player.velocity.y > 0

