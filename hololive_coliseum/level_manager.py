from .player import (
    GuraPlayer,
    WatsonPlayer,
    InaPlayer,
    KiaraPlayer,
    CalliopePlayer,
    FaunaPlayer,
    KroniiPlayer,
    IRySPlayer,
    MumeiPlayer,
    BaelzPlayer,
    FubukiPlayer,
    MikoPlayer,
    AquaPlayer,
    PekoraPlayer,
    MarinePlayer,
    SuiseiPlayer,
    AyamePlayer,
    NoelPlayer,
    FlarePlayer,
    SubaruPlayer,
    SoraPlayer,
    Enemy,
)
from .gravity_zone import GravityZone


class LevelManager:
    """Handle level initialization and reset logic."""

    def __init__(self, game):
        self.game = game

    def setup_level(self) -> None:
        """Initialize or reset gameplay objects for the current selection."""
        g = self.game
        g.final_time = 0
        g.end_time = 0
        g.show_end_options = False
        g.status_manager._effects.clear()
        g.score = 0
        import os
        import pygame
        image_dir = os.path.join(os.path.dirname(__file__), "..", "Images")
        char_map = {
            "Watson Amelia": (WatsonPlayer, "Watson_Amelia_right.png"),
            "Ninomae Ina'nis": (InaPlayer, "Ninomae_Inanis_right.png"),
            "Takanashi Kiara": (KiaraPlayer, "Takanashi_Kiara_right.png"),
            "Mori Calliope": (CalliopePlayer, "Mori_Calliope_right.png"),
            "Ceres Fauna": (FaunaPlayer, "Ceres_Fauna_right.png"),
            "Ouro Kronii": (KroniiPlayer, "Ouro_Kronii_right.png"),
            "IRyS": (IRySPlayer, "IRyS_right.png"),
            "Nanashi Mumei": (MumeiPlayer, "Nanashi_Mumei_right.png"),
            "Hakos Baelz": (BaelzPlayer, "Hakos_Baelz_right.png"),
            "Shirakami Fubuki": (FubukiPlayer, "Shirakami_Fubuki_right.png"),
            "Sakura Miko": (MikoPlayer, "Sakura_Miko_right.png"),
            "Minato Aqua": (AquaPlayer, "Minato_Aqua_right.png"),
            "Usada Pekora": (PekoraPlayer, "Usada_Pekora_right.png"),
            "Houshou Marine": (MarinePlayer, "Houshou_Marine_right.png"),
            "Hoshimachi Suisei": (SuiseiPlayer, "Hoshimachi_Suisei_right.png"),
            "Nakiri Ayame": (AyamePlayer, "Nakiri_Ayame_right.png"),
            "Shirogane Noel": (NoelPlayer, "Shirogane_Noel_right.png"),
            "Shiranui Flare": (FlarePlayer, "Shiranui_Flare_right.png"),
            "Oozora Subaru": (SubaruPlayer, "Oozora_Subaru_right.png"),
            "Tokino Sora": (SoraPlayer, "Tokino_Sora_right.png"),
        }
        player_cls, img_name = char_map.get(
            g.selected_character, (GuraPlayer, "Gawr_Gura_right.png")
        )
        img = os.path.join(image_dir, img_name)
        g.player = player_cls(100, g.ground_y - 60, img)
        g.difficulty = g.difficulty_levels[g.difficulty_index]
        g.all_sprites = pygame.sprite.Group(g.player)
        g.projectiles = pygame.sprite.Group()
        g.melee_attacks = pygame.sprite.Group()
        g.gravity_zones = pygame.sprite.Group()
        g.healing_zones = pygame.sprite.Group()
        g.hazard_manager.clear()
        g.hazards = g.hazard_manager.hazards
        g.powerups = pygame.sprite.Group()
        g.enemies = pygame.sprite.Group()
        g.npc_manager.enemies = g.enemies
        g.npc_manager.allies.empty()
        g.ai_manager.enemies = g.enemies
        g.spawn_manager.clear()
        g.combat_manager.last_enemy_damage = 0
        g.hazard_manager.last_damage = 0
        for i in range(g.ai_players):
            e = Enemy(
                300 + i * 60,
                g.ground_y - 60,
                os.path.join(image_dir, "enemy_right.png"),
                difficulty=g.difficulty,
            )
            e.last_ai_action = -e.AI_LEVELS[g.difficulty]["react_ms"]
            g.enemies.add(e)
            g.all_sprites.add(e)
        map_data = g.map_manager.get_current() or {}
        for gz in map_data.get("gravity_zones", []):
            rect = pygame.Rect(*gz["rect"])
            zone = GravityZone(rect, gz.get("multiplier", 1.0))
            g.gravity_zones.add(zone)
            g.all_sprites.add(zone)
        g.hazard_manager.load_from_data(map_data.get("hazards", []))
        for h in g.hazard_manager.hazards:
            g.all_sprites.add(h)
        now = pygame.time.get_ticks()
        g.spawn_manager.schedule("heal", now + 5000)
