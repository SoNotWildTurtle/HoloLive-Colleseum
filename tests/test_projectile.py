import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from hololive_coliseum.projectile import Projectile, PROJECTILE_SPEED
from hololive_coliseum.melee_attack import MeleeAttack, MELEE_LIFETIME


def test_projectile_moves():
    proj = Projectile(0, 0, 1)
    orig_x = proj.rect.x
    proj.update()
    assert proj.rect.x == orig_x + PROJECTILE_SPEED


def test_melee_attack_lifetime():
    attack = MeleeAttack(0, 0, 1)
    for _ in range(MELEE_LIFETIME):
        attack.update()
    # Should be killed after lifetime expires
    assert not attack.alive()
