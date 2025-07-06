GRAVITY = 0.5
MAX_FALL_SPEED = 15
MOVE_ACCEL = 0.5
MAX_MOVE_SPEED = 5
GROUND_FRICTION = 0.4
AIR_FRICTION = 0.1


def apply_gravity(vy: float, multiplier: float = 1.0) -> float:
    """Apply gravity and limit to MAX_FALL_SPEED."""
    vy += GRAVITY * multiplier
    if vy > MAX_FALL_SPEED:
        vy = MAX_FALL_SPEED
    return vy


def accelerate(vx: float, direction: int) -> float:
    """Accelerate horizontally up to MAX_MOVE_SPEED."""
    vx += MOVE_ACCEL * direction
    if vx > MAX_MOVE_SPEED:
        vx = MAX_MOVE_SPEED
    elif vx < -MAX_MOVE_SPEED:
        vx = -MAX_MOVE_SPEED
    return vx


def apply_friction(vx: float, on_ground: bool) -> float:
    """Apply friction to slow down when no input."""
    friction = GROUND_FRICTION if on_ground else AIR_FRICTION
    if vx > 0:
        vx = max(0, vx - friction)
    elif vx < 0:
        vx = min(0, vx + friction)
    return vx
