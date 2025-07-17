class HazardManager:
    """Manage hazard sprites and apply effects."""
    def __init__(self):
        import pygame
        self.hazards = pygame.sprite.Group()
        self.last_damage = 0

    def load_from_data(self, hazard_data):
        """Create hazard sprites from map metadata."""
        import pygame
        from .hazards import SpikeTrap, IceZone, LavaZone
        self.hazards.empty()
        hazard_map = {
            "spike": SpikeTrap,
            "ice": IceZone,
            "lava": LavaZone,
        }
        for hd in hazard_data:
            rect = pygame.Rect(*hd["rect"])
            cls = hazard_map.get(hd.get("type"), SpikeTrap)
            self.hazards.add(cls(rect))

    def apply_to_player(self, player, now):
        import pygame
        from .hazards import SpikeTrap, IceZone, LavaZone
        hz = pygame.sprite.spritecollideany(player, self.hazards)
        if hz:
            if isinstance(hz, SpikeTrap) and now - self.last_damage >= 500:
                player.take_damage(hz.damage)
                self.last_damage = now
            elif isinstance(hz, LavaZone) and now - self.last_damage >= hz.interval:
                player.take_damage(hz.damage)
                self.last_damage = now
            elif isinstance(hz, IceZone):
                player.set_friction_multiplier(hz.friction)
                return
        player.set_friction_multiplier(1.0)

    def apply_to_enemy(self, enemy, now):
        import pygame
        from .hazards import SpikeTrap, LavaZone
        hz = pygame.sprite.spritecollideany(enemy, self.hazards)
        if isinstance(hz, SpikeTrap):
            enemy.take_damage(hz.damage)
            if enemy.health == 0:
                enemy.kill()
                return True
        elif isinstance(hz, LavaZone) and now - self.last_damage >= hz.interval:
            enemy.take_damage(hz.damage)
            self.last_damage = now
        return False

    def clear(self):
        self.hazards.empty()
        self.last_damage = 0
