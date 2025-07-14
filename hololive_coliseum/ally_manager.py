class AllyManager:
    """Simple manager for friendly NPCs that follow the player."""

    def __init__(self, allies) -> None:
        self.allies = allies

    def update(self, player, ground_y: int, now: int) -> None:
        for ally in list(self.allies):
            if hasattr(ally, "handle_ai"):
                ally.handle_ai(player, now)
            else:
                direction = 1 if player.rect.centerx > ally.rect.centerx else -1
                ally.velocity.x = direction
            ally.update(ground_y, now)
