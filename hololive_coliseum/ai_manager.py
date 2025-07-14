class AIManager:
    """Coordinate AI updates for enemy sprites."""

    def __init__(self, enemies) -> None:
        self.enemies = enemies

    def update(self, player, now, hazards=None, projectiles=None):
        """Run AI logic for all enemies and return actions."""
        hazards = hazards or []
        projectiles = projectiles or []
        new_projectiles = []
        new_melees = []
        for enemy in list(self.enemies):
            proj, melee = enemy.handle_ai(player, now, hazards, projectiles)
            if proj:
                new_projectiles.append((enemy, proj))
            if melee:
                new_melees.append((enemy, melee))
        return new_projectiles, new_melees
