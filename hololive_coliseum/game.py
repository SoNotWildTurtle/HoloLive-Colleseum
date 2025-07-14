import os
import pygame

from .player import (
    PlayerCharacter,
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
from .projectile import Projectile, ExplodingProjectile
from .melee_attack import MeleeAttack
from .gravity_zone import GravityZone
from .hazards import SpikeTrap, IceZone, LavaZone
from .powerup import PowerUp
from .healing_zone import HealingZone
from .save_manager import load_settings, save_settings, wipe_saves
from .network import NetworkManager
from .node_registry import load_nodes
from .keybind_manager import KeybindManager
from .chat_manager import ChatManager
from .menus import MenuMixin, MENU_BG_COLOR, MENU_TEXT_COLOR
from .accounts import register_account, delete_account
from .status_effects import StatusEffectManager, FreezeEffect, SlowEffect
from .ai_manager import AIManager
from .npc_manager import NPCManager
from .ally_manager import AllyManager
from .menu_manager import MenuManager
from .game_state_manager import GameStateManager


class Game(MenuMixin):
    """Main game class with menus, AI opponents, networking and settings."""

    def __init__(self, width: int = 800, height: int = 600):
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        pygame.init()
        self.settings = load_settings()
        self.width = self.settings.get("width", width)
        self.height = self.settings.get("height", height)
        self.volume = self.settings.get("volume", 1.0)
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        self.mixer_ready = False
        try:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(self.volume)
            self.mixer_ready = True
        except pygame.error:
            self.mixer_ready = False
        default_keys = {
            "shoot": pygame.K_z,
            "melee": pygame.K_x,
            "jump": pygame.K_SPACE,
            "block": pygame.K_LSHIFT,
            "parry": pygame.K_c,
            "dodge": pygame.K_LCTRL,
            "special": pygame.K_v,
        }
        self.keybind_manager = KeybindManager(default_keys)
        self.keybind_manager.load_from_dict(self.settings.get("key_bindings", {}))
        self.key_bindings = self.keybind_manager.bindings
        self.chat_manager = ChatManager()
        self.chat_input = ""
        pygame.joystick.init()
        self.joysticks = [
            pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
        ]
        for j in self.joysticks:
            j.init()
        default_controller = {
            "shoot": 0,
            "melee": 1,
            "jump": 2,
            "block": 4,
            "parry": 5,
            "dodge": 6,
            "special": 3,
        }
        self.controller_bindings = self.settings.get(
            "controller_bindings", default_controller
        )
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Hololive Coliseum")
        self.clock = pygame.time.Clock()
        self.running = False
        self.state = "splash"  # splash -> main_menu -> howto/credits/scoreboard -> mode -> solo_multi -> mp_type -> char -> lobby -> map/chapter -> settings -> accounts -> playing -> paused -> victory/game_over
        self.menu_index = 0
        self.state_manager = GameStateManager(self.state)
        self.menu_manager = MenuManager()
        self.main_menu_options = [
            "New Game",
            "Settings",
            "How to Play",
            "Credits",
            "Records",
            "Exit",
        ]
        self.mode_options = ["Story", "Arena", "Custom", "Back"]
        self.solo_multi_options = ["Solo", "Multiplayer", "Back"]
        self.mp_type_options = ["Offline", "Online", "Back"]
        self.online_multiplayer = False
        self.pause_options = ["Resume", "Main Menu"]
        self.game_over_options = ["Play Again", "Main Menu"]
        self.victory_options = ["Play Again", "Main Menu"]
        self.final_time = 0
        self.end_time = 0
        self.show_end_options = False
        self.best_time = self.settings.get("best_time", 0)
        self.best_score = self.settings.get("best_score", 0)
        self.score = 0
        self.show_fps = self.settings.get("show_fps", False)
        self.settings_options = [
            "Key Bindings",
            "Controller Bindings",
            "Window Size",
            "Volume",
            "Show FPS",
            "Reset Records",
            "Wipe Saves",
            "Node Settings",
            "Accounts",
            "Back",
        ]
        self.info_options = ["Back"]
        self.key_options = [
            "jump",
            "shoot",
            "melee",
            "block",
            "parry",
            "dodge",
            "special",
            "Back",
        ]
        self.controller_options = list(self.key_options)
        self.rebind_action: str | None = None
        self.node_options = ["Start Node", "Stop Node", "Latency Helper", "Back"]
        self.account_options = ["Register Account", "Delete Account", "Back"]
        self.account_id = "player"
        self.network_manager: NetworkManager | None = None
        self.node_hosting = False
        self.latency_helper = False
        self.characters = [
            "Gawr Gura",
            "Watson Amelia",
            "Ninomae Ina'nis",
            "Takanashi Kiara",
            "Mori Calliope",
            "Ceres Fauna",
            "Ouro Kronii",
            "IRyS",
            "Nanashi Mumei",
            "Hakos Baelz",
            "Shirakami Fubuki",
            "Sakura Miko",
            "Minato Aqua",
            "Usada Pekora",
            "Houshou Marine",
            "Hoshimachi Suisei",
            "Nakiri Ayame",
            "Shirogane Noel",
            "Shiranui Flare",
            "Oozora Subaru",
            "Tokino Sora",
        ]
        self.maps = ["Default"]
        self.chapters = [f"Chapter {i}" for i in range(1, 21)]
        self.difficulty_levels = ["Easy", "Normal", "Hard"]
        self.difficulty_index = 1
        self.character_menu_options = self.characters + [
            "Add AI Player",
            "Difficulty",
            "Continue",
            "Back",
        ]
        self.map_menu_options = self.maps + ["Back"]
        self.chapter_menu_options = self.chapters + ["Back"]
        self.lobby_options = ["Start Game", "Back"]
        self.human_players = 1
        self.ai_players = 0
        self.player_names = ["Player 1"]
        self.multiplayer = False
        self.selected_mode: str | None = None
        self.selected_character: str | None = None
        self.selected_map: str | None = None
        self.selected_chapter: str | None = None
        image_dir = os.path.join(os.path.dirname(__file__), "..", "Images")

        def _create_icon(text: str, size=(64, 64)) -> pygame.Surface:
            surf = pygame.Surface(size)
            surf.fill((200, 200, 200))
            font = pygame.font.SysFont(None, 20)
            label = font.render(text, True, (0, 0, 0))
            surf.blit(label, label.get_rect(center=(size[0] // 2, size[1] // 2)))
            return surf

        def _load(name: str, size=(64, 64)) -> pygame.Surface:
            path = os.path.join(image_dir, name)
            if os.path.exists(path):
                return pygame.image.load(path).convert_alpha()
            return _create_icon(os.path.splitext(name)[0], size)

        self.character_images = {
            "Gawr Gura": _load("Gawr_Gura_right.png"),
            "Watson Amelia": _load("Watson_Amelia_right.png"),
            "Ninomae Ina'nis": _load("Ninomae_Inanis_right.png"),
            "Takanashi Kiara": _load("Takanashi_Kiara_right.png"),
            "Mori Calliope": _load("Mori_Calliope_right.png"),
            "Ceres Fauna": _load("Ceres_Fauna_right.png"),
            "Ouro Kronii": _load("Ouro_Kronii_right.png"),
            "IRyS": _load("IRyS_right.png"),
            "Nanashi Mumei": _load("Nanashi_Mumei_right.png"),
            "Hakos Baelz": _load("Hakos_Baelz_right.png"),
            "Shirakami Fubuki": _load("Shirakami_Fubuki_right.png"),
            "Sakura Miko": _load("Sakura_Miko_right.png"),
            "Minato Aqua": _load("Minato_Aqua_right.png"),
            "Usada Pekora": _load("Usada_Pekora_right.png"),
            "Houshou Marine": _load("Houshou_Marine_right.png"),
            "Hoshimachi Suisei": _load("Hoshimachi_Suisei_right.png"),
            "Nakiri Ayame": _load("Nakiri_Ayame_right.png"),
            "Shirogane Noel": _load("Shirogane_Noel_right.png"),
            "Shiranui Flare": _load("Shiranui_Flare_right.png"),
            "Oozora Subaru": _load("Oozora_Subaru_right.png"),
            "Tokino Sora": _load("Tokino_Sora_right.png"),
        }
        self.map_images = {
            "Default": _load("map_default.png"),
        }
        self.chapter_images = {
            f"Chapter {i}": _load(f"chapter{i}.png") for i in range(1, 21)
        }
        self.title_font = pygame.font.SysFont(None, 64)
        self.menu_font = pygame.font.SysFont(None, 32)
        self.menu_drawers = {
            "splash": self._draw_menu,
            "main_menu": lambda: self._draw_option_menu("Main Menu", self.main_menu_options),
            "mode": lambda: self._draw_option_menu("Game Type", self.mode_options),
            "solo_multi": lambda: self._draw_option_menu("Players", self.solo_multi_options),
            "mp_type": lambda: self._draw_option_menu("Multiplayer", self.mp_type_options),
            "char": self._draw_character_menu,
            "map": self._draw_map_menu,
            "chapter": self._draw_chapter_menu,
            "lobby": self._draw_lobby_menu,
            "settings": self._draw_settings_menu,
            "key_bindings": self._draw_key_bindings_menu,
            "controller_bindings": self._draw_controller_bindings_menu,
            "rebind": self._draw_rebind_prompt,
            "rebind_controller": self._draw_rebind_controller_prompt,
            "node_settings": self._draw_node_menu,
            "accounts": self._draw_accounts_menu,
            "howto": self._draw_how_to_play,
            "credits": self._draw_credits,
            "scoreboard": self._draw_scoreboard_menu,
            "paused": self._draw_pause_menu,
            "victory": self._draw_victory_menu,
            "game_over": self._draw_game_over_menu,
        }

        # Stage setup
        self.ground_y = self.height - 50
        self.next_powerup_time = 0
        self.last_enemy_damage = 0
        self.level_start_time = 0
        self.level_limit = 60  # seconds
        self.status_manager = StatusEffectManager()
        self.npc_manager = NPCManager()
        self.ai_manager = AIManager(self.npc_manager.enemies)
        self.ally_manager = AllyManager(self.npc_manager.allies)
        self._setup_level()

    def _setup_level(self) -> None:
        """Initialize or reset gameplay objects based on the chosen character."""
        self.final_time = 0
        self.end_time = 0
        self.show_end_options = False
        self.status_manager._effects.clear()
        self.score = 0
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
            self.selected_character, (GuraPlayer, "Gawr_Gura_right.png")
        )
        img = os.path.join(image_dir, img_name)
        self.player = player_cls(100, self.ground_y - 60, img)
        self.difficulty = self.difficulty_levels[self.difficulty_index]
        self.all_sprites = pygame.sprite.Group(self.player)
        self.projectiles = pygame.sprite.Group()
        self.melee_attacks = pygame.sprite.Group()
        self.gravity_zones = pygame.sprite.Group()
        self.healing_zones = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.npc_manager.enemies = self.enemies
        self.npc_manager.allies.empty()
        self.ai_manager.enemies = self.enemies
        # Reset timers when starting a new level
        self.next_powerup_time = 0
        self.last_enemy_damage = 0
        self.last_hazard_damage = 0
        for i in range(self.ai_players):
            e = Enemy(
                300 + i * 60,
                self.ground_y - 60,
                os.path.join(image_dir, "enemy_right.png"),
                difficulty=self.difficulty,
            )
            e.last_ai_action = -e.AI_LEVELS[self.difficulty]["react_ms"]
            self.enemies.add(e)
            self.all_sprites.add(e)

        zone_rect = pygame.Rect(self.width // 2 - 50, self.ground_y - 150, 100, 50)
        self.low_gravity_zone = GravityZone(zone_rect, 0.2)
        self.gravity_zones.add(self.low_gravity_zone)
        self.all_sprites.add(self.low_gravity_zone)
        high_rect = pygame.Rect(self.width // 2 + 70, self.ground_y - 120, 80, 40)
        self.high_gravity_zone = GravityZone(high_rect, 2.0)
        self.gravity_zones.add(self.high_gravity_zone)
        self.all_sprites.add(self.high_gravity_zone)
        spike = SpikeTrap(pygame.Rect(self.width // 3, self.ground_y - 20, 40, 20))
        ice = IceZone(pygame.Rect(self.width // 2 + 80, self.ground_y - 20, 60, 20))
        lava = LavaZone(pygame.Rect(self.width // 2 - 100, self.ground_y - 20, 60, 20))
        self.hazards.add(spike, ice, lava)
        self.all_sprites.add(spike, ice, lava)

    def _cycle_volume(self) -> None:
        """Cycle master volume between 0%, 50% and 100%."""
        steps = [0.0, 0.5, 1.0]
        current = min(steps, key=lambda v: abs(v - self.volume))
        idx = steps.index(current)
        self.volume = steps[(idx + 1) % len(steps)]
        if self.mixer_ready:
            pygame.mixer.music.set_volume(self.volume)

    def _set_state(self, state: str) -> None:
        """Helper to update game and managers with a new state."""
        self.state = state
        self.state_manager.change(state)
        self.menu_manager.reset()
        self.menu_index = self.menu_manager.index

    def execute_account_option(self, option: str) -> None:
        """Handle register/delete actions for tests and menus."""
        if option == "Register Account":
            register_account(self.account_id, "user", "PUBKEY")
        elif option == "Delete Account":
            delete_account(self.account_id)

    def start_node(self) -> None:
        """Begin hosting a blockchain node."""
        if self.network_manager is None:
            self.network_manager = NetworkManager(host=True, relay_mode=self.latency_helper)
            self.network_manager.broadcast_announce(load_nodes())
            if self.latency_helper:
                self.network_manager.offer_relay(load_nodes())
            self.node_hosting = True

    def stop_node(self) -> None:
        """Stop hosting the blockchain node."""
        if self.network_manager is not None:
            try:
                self.network_manager.sock.close()
            except OSError:
                pass
            self.network_manager = None
        self.node_hosting = False

    def _poll_network(self) -> None:
        if self.network_manager is not None:
            self.network_manager.poll()
            self.network_manager.process_reliable()

    def _handle_collisions(self) -> None:
        """Handle combat collisions between attacks and sprites."""
        now = pygame.time.get_ticks()
        for proj in list(self.projectiles):
            if getattr(proj, "from_enemy", False):
                if self.player.rect.colliderect(proj.rect):
                    if getattr(self.player, "shield_active", False):
                        proj.kill()
                    else:
                        self.player.take_damage(10)
                        proj.kill()
                continue
            hits = pygame.sprite.spritecollide(proj, self.enemies, False)
            if hits:
                for enemy in hits:
                    if getattr(proj, "grapple", False):
                        enemy.rect.centerx = self.player.rect.centerx
                        enemy.pos.x = enemy.rect.x
                    elif getattr(proj, "freeze", False):
                        self.status_manager.add_effect(enemy, FreezeEffect())
                        enemy.take_damage(5)
                    elif getattr(proj, "slow", False):
                        self.status_manager.add_effect(enemy, SlowEffect())
                        enemy.take_damage(5)
                    else:
                        enemy.take_damage(10)
                    if enemy.health == 0:
                        enemy.kill()
                        self.score += 1
                if not getattr(proj, "pierce", False):
                    proj.kill()
        for attack in list(self.melee_attacks):
            if getattr(attack, "from_enemy", False):
                if attack.rect.colliderect(self.player.rect):
                    self.player.take_damage(15)
                attack.kill()
                continue
            hits = pygame.sprite.spritecollide(attack, self.enemies, False)
            if hits:
                for enemy in hits:
                    enemy.take_damage(15)
                    if enemy.health == 0:
                        enemy.kill()
                        self.score += 1
            attack.kill()
        if (
            pygame.sprite.spritecollideany(self.player, self.enemies)
            and now - self.last_enemy_damage >= 500
        ):
            self.player.take_damage(10)
            self.last_enemy_damage = now

    def run(self):
        """Start the main game loop."""
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.state == "splash" and event.type in (
                    pygame.KEYDOWN,
                    pygame.MOUSEBUTTONDOWN,
                    pygame.JOYBUTTONDOWN,
                ):
                    self._set_state("main_menu")
                    self.menu_index = 0
                elif (
                    self.state == "playing"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    self._set_state("paused")
                    self.menu_index = 0
                elif (
                    self.state == "paused"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    self._set_state("playing")
                elif (
                    self.state == "playing"
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN
                ):
                    if self.chat_manager.open:
                        if self.chat_input.strip():
                            sender = self.player_names[0] if self.player_names else "Player"
                            self.chat_manager.send(sender, self.chat_input)
                        self.chat_input = ""
                        self.chat_manager.hide()
                    else:
                        self.chat_manager.show()
                    continue
                elif (
                    self.state == "playing"
                    and self.chat_manager.open
                    and event.type == pygame.KEYDOWN
                ):
                    if event.key == pygame.K_BACKSPACE:
                        self.chat_input = self.chat_input[:-1]
                    elif event.unicode and event.unicode.isprintable():
                        self.chat_input += event.unicode
                    continue
                elif (
                    self.state
                    in {
                        "main_menu",
                        "mode",
                        "solo_multi",
                        "settings",
                        "key_bindings",
                        "controller_bindings",
                        "char",
                        "map",
                        "chapter",
                        "mp_type",
                        "paused",
                        "victory",
                        "game_over",
                    }
                    and event.type == pygame.KEYDOWN
                    and (
                        self.state not in {"victory", "game_over"}
                        or self.show_end_options
                    )
                ):
                    options = {
                        "main_menu": self.main_menu_options,
                        "mode": self.mode_options,
                        "solo_multi": self.solo_multi_options,
                        "mp_type": self.mp_type_options,
                        "settings": self.settings_options,
                        "node_settings": self.node_options,
                        "accounts": self.account_options,
                        "howto": self.info_options,
                        "credits": self.info_options,
                        "scoreboard": self.info_options,
                        "key_bindings": self.key_options,
                        "controller_bindings": self.controller_options,
                        "char": self.character_menu_options,
                        "map": self.map_menu_options,
                        "chapter": self.chapter_menu_options,
                        "lobby": self.lobby_options,
                        "paused": self.pause_options,
                        "victory": self.victory_options,
                        "game_over": self.game_over_options,
                    }[self.state]
                    if (
                        self.state == "char"
                        and event.key == pygame.K_j
                        and self.multiplayer
                        and not self.online_multiplayer
                    ):
                        if self.human_players < 4:
                            self.human_players += 1
                            self.player_names.append(f"Player {self.human_players}")
                        continue
                    if event.key == pygame.K_UP:
                        self.menu_manager.move(-1, len(options))
                        self.menu_index = self.menu_manager.index
                    elif event.key == pygame.K_DOWN:
                        self.menu_manager.move(1, len(options))
                        self.menu_index = self.menu_manager.index
                    elif (
                        self.state == "char"
                        and options[self.menu_index] == "Difficulty"
                        and event.key in (pygame.K_LEFT, pygame.K_RIGHT)
                    ):
                        if event.key == pygame.K_LEFT:
                            self.difficulty_index = (self.difficulty_index - 1) % len(
                                self.difficulty_levels
                            )
                        else:
                            self.difficulty_index = (self.difficulty_index + 1) % len(
                                self.difficulty_levels
                            )
                    elif (
                        self.state == "settings"
                        and options[self.menu_index] == "Volume"
                        and event.key in (pygame.K_LEFT, pygame.K_RIGHT)
                    ):
                        if event.key == pygame.K_LEFT:
                            self.volume = max(0.0, self.volume - 0.1)
                        else:
                            self.volume = min(1.0, self.volume + 0.1)
                        if self.mixer_ready:
                            pygame.mixer.music.set_volume(self.volume)
                    elif (
                        self.state == "key_bindings"
                        and options[self.menu_index] != "Back"
                        and event.key in (pygame.K_RETURN, pygame.K_SPACE)
                    ):
                        self.rebind_action = options[self.menu_index]
                        self._set_state("rebind")
                    elif (
                        self.state == "controller_bindings"
                        and options[self.menu_index] != "Back"
                        and event.key in (pygame.K_RETURN, pygame.K_SPACE)
                    ):
                        self.rebind_action = options[self.menu_index]
                        self._set_state("rebind_controller")
                    elif (
                        self.state == "key_bindings"
                        and options[self.menu_index] == "Back"
                        and event.key in (pygame.K_RETURN, pygame.K_SPACE)
                    ):
                        self._set_state("settings")
                        self.menu_index = 0
                    elif (
                        self.state == "controller_bindings"
                        and options[self.menu_index] == "Back"
                        and event.key in (pygame.K_RETURN, pygame.K_SPACE)
                    ):
                        self._set_state("settings")
                        self.menu_index = 0
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        choice = options[self.menu_index]
                        if self.state == "main_menu":
                            if choice == "New Game":
                                self._set_state("mode")
                                self.menu_index = 0
                            elif choice == "Settings":
                                self._set_state("settings")
                                self.menu_index = 0
                            elif choice == "How to Play":
                                self._set_state("howto")
                                self.menu_index = 0
                            elif choice == "Credits":
                                self._set_state("credits")
                                self.menu_index = 0
                            elif choice == "Records":
                                self._set_state("scoreboard")
                                self.menu_index = 0
                            elif choice == "Exit":
                                self.running = False
                        elif self.state == "mode":
                            if choice == "Back":
                                self._set_state("main_menu")
                                self.menu_index = 0
                            else:
                                self.selected_mode = choice
                                self.human_players = 1
                                self.ai_players = 0
                                self._set_state("solo_multi")
                                self.menu_index = 0
                        elif self.state == "solo_multi":
                            if choice == "Back":
                                self._set_state("mode")
                                self.menu_index = 0
                            else:
                                self.multiplayer = choice == "Multiplayer"
                                if choice == "Solo":
                                    self._set_state("char")
                                else:
                                    self._set_state("mp_type")
                                self.menu_index = 0
                        elif self.state == "mp_type":
                            if choice == "Back":
                                self._set_state("solo_multi")
                                self.menu_index = 0
                            else:
                                self.online_multiplayer = choice == "Online"
                                self._set_state("char")
                                self.menu_index = 0
                        elif self.state == "char":
                            if choice == "Add AI Player":
                                if self.ai_players < 4 - self.human_players:
                                    self.ai_players += 1
                            elif choice == "Difficulty":
                                self.difficulty_index = (
                                    self.difficulty_index + 1
                                ) % len(self.difficulty_levels)
                            elif choice == "Continue":
                                if self.selected_character is None and self.characters:
                                    self.selected_character = self.characters[0]
                                if self.multiplayer:
                                    self.player_names = [
                                        f"Player {i+1}"
                                        for i in range(self.human_players)
                                    ]
                                    self.player_names += [
                                        f"AI {i+1}" for i in range(self.ai_players)
                                    ]
                                    self._set_state("lobby")
                                elif self.selected_mode == "Story":
                                    self._set_state("chapter")
                                else:
                                    self._set_state("map")
                                self.menu_index = 0
                            elif choice == "Back":
                                self.state = (
                                    "mp_type" if self.multiplayer else "solo_multi"
                                )
                                self.menu_index = 0
                            else:
                                self.selected_character = choice
                        elif self.state == "lobby":
                            if choice == "Back":
                                self._set_state("char")
                                self.menu_index = 0
                            elif choice == "Start Game":
                                if self.selected_mode == "Story":
                                    self._set_state("chapter")
                                else:
                                    self._set_state("map")
                                self.menu_index = 0
                        elif self.state == "map":
                            if choice == "Back":
                                if self.multiplayer:
                                    self._set_state("lobby")
                                else:
                                    self._set_state("char")
                                self.menu_index = 0
                            else:
                                self.selected_map = choice
                                self._setup_level()
                                self._set_state("playing")
                                self.level_start_time = pygame.time.get_ticks()
                        elif self.state == "chapter":
                            if choice == "Back":
                                if self.multiplayer:
                                    self._set_state("lobby")
                                else:
                                    self._set_state("char")
                                self.menu_index = 0
                            else:
                                self.selected_chapter = choice
                                self._setup_level()
                                self._set_state("playing")
                                self.level_start_time = pygame.time.get_ticks()
                        elif self.state == "settings":
                            if choice == "Back":
                                self._set_state("main_menu")
                                self.menu_index = 0
                            elif choice == "Key Bindings":
                                self._set_state("key_bindings")
                                self.menu_index = 0
                            elif choice == "Controller Bindings":
                                self._set_state("controller_bindings")
                                self.menu_index = 0
                            elif choice == "Window Size":
                                if (self.width, self.height) == (800, 600):
                                    self.width, self.height = 1024, 768
                                else:
                                    self.width, self.height = 800, 600
                                self.screen = pygame.display.set_mode(
                                    (self.width, self.height)
                                )
                            elif choice == "Volume":
                                self._cycle_volume()
                            elif choice == "Show FPS":
                                self.show_fps = not self.show_fps
                            elif choice == "Reset Records":
                                self.best_time = 0
                                self.best_score = 0
                            elif choice == "Wipe Saves":
                                wipe_saves()
                            elif choice == "Node Settings":
                                self._set_state("node_settings")
                                self.menu_index = 0
                            elif choice == "Accounts":
                                self._set_state("accounts")
                                self.menu_index = 0
                        elif self.state == "node_settings":
                            if choice == "Back":
                                self._set_state("settings")
                                self.menu_index = 0
                            elif choice == "Start Node":
                                self.start_node()
                            elif choice == "Stop Node":
                                self.stop_node()
                            elif choice == "Latency Helper":
                                self.latency_helper = not self.latency_helper
                                if self.network_manager is not None:
                                    self.network_manager.relay_mode = self.latency_helper
                                    if self.latency_helper:
                                        self.network_manager.offer_relay(load_nodes())
                        elif self.state == "accounts":
                            if choice == "Back":
                                self._set_state("settings")
                                self.menu_index = 0
                            elif choice == "Register Account":
                                self.execute_account_option("Register Account")
                            elif choice == "Delete Account":
                                self.execute_account_option("Delete Account")
                        elif self.state in {"howto", "credits", "scoreboard"}:
                            if choice == "Back":
                                self._set_state("main_menu")
                                self.menu_index = 0
                        elif self.state == "paused":
                            if choice == "Resume":
                                self._set_state("playing")
                            elif choice == "Main Menu":
                                self._set_state("main_menu")
                                self.menu_index = 0
                        elif self.state == "game_over":
                            if choice == "Play Again":
                                self._set_state("char")
                                self.menu_index = 0
                            elif choice == "Main Menu":
                                self._set_state("main_menu")
                                self.menu_index = 0
                        elif self.state == "victory":
                            if choice == "Play Again":
                                self._set_state("char")
                                self.menu_index = 0
                            elif choice == "Main Menu":
                                self._set_state("main_menu")
                                self.menu_index = 0
                elif self.state == "rebind" and event.type == pygame.KEYDOWN:
                    self.keybind_manager.set(self.rebind_action, event.key)
                    self._set_state("key_bindings")
                elif (
                    self.state == "rebind_controller"
                    and event.type == pygame.JOYBUTTONDOWN
                ):
                    self.controller_bindings[self.rebind_action] = event.button
                    self._set_state("controller_bindings")
            now = pygame.time.get_ticks()
            self.status_manager.update(now)
            if (
                self.state in {"victory", "game_over"}
                and not self.show_end_options
                and now - self.end_time >= 3000
            ):
                self.show_end_options = True

            drawer = self.menu_drawers.get(self.state)
            if drawer is not None:
                drawer()
            else:
                keys = pygame.key.get_pressed()

                def action_pressed(action: str) -> bool:
                    key = self.keybind_manager.get(action)
                    if key is not None and keys[key]:
                        return True
                    for joy in self.joysticks:
                        btn = self.controller_bindings.get(action)
                        if btn is not None and joy.get_button(btn):
                            return True
                    return False

                self.player.handle_input(keys, now, self.keybind_manager.bindings, action_pressed)
                if action_pressed("special"):
                    proj = self.player.special_attack(now)
                    if isinstance(proj, HealingZone):
                        self.healing_zones.add(proj)
                        self.all_sprites.add(proj)
                    elif proj:
                        self.projectiles.add(proj)
                        self.all_sprites.add(proj)
                if action_pressed("shoot"):
                    proj = self.player.shoot(now, pygame.mouse.get_pos())
                    if proj:
                        self.projectiles.add(proj)
                        self.all_sprites.add(proj)
                if action_pressed("melee"):
                    melee = self.player.melee_attack(now)
                    if melee:
                        self.melee_attacks.add(melee)
                        self.all_sprites.add(melee)
                zone = pygame.sprite.spritecollideany(self.player, self.gravity_zones)
                if zone:
                    self.player.set_gravity_multiplier(zone.multiplier)
                else:
                    self.player.set_gravity_multiplier(1.0)
                hazard = pygame.sprite.spritecollideany(self.player, self.hazards)
                if hazard:
                    if isinstance(hazard, SpikeTrap) and now - self.last_hazard_damage >= 500:
                        self.player.take_damage(hazard.damage)
                        self.last_hazard_damage = now
                    if isinstance(hazard, LavaZone) and now - self.last_hazard_damage >= hazard.interval:
                        self.player.take_damage(hazard.damage)
                        self.last_hazard_damage = now
                    if isinstance(hazard, IceZone):
                        self.player.set_friction_multiplier(hazard.friction)
                else:
                    self.player.set_friction_multiplier(1.0)
                extra = self.player.update(self.ground_y, now)
                if isinstance(extra, pygame.sprite.Sprite):
                    self.projectiles.add(extra)
                    self.all_sprites.add(extra)
                new_projs, new_melees = self.ai_manager.update(
                    self.player, now, self.hazards, self.projectiles
                )
                for enemy, proj in new_projs:
                    self.projectiles.add(proj)
                    self.all_sprites.add(proj)
                for enemy, melee in new_melees:
                    self.melee_attacks.add(melee)
                    self.all_sprites.add(melee)
                for enemy in list(self.enemies):
                    zone = pygame.sprite.spritecollideany(enemy, self.gravity_zones)
                    if zone:
                        enemy.set_gravity_multiplier(zone.multiplier)
                    else:
                        enemy.set_gravity_multiplier(1.0)
                    hz = pygame.sprite.spritecollideany(enemy, self.hazards)
                    if isinstance(hz, SpikeTrap):
                        enemy.take_damage(hz.damage)
                        if enemy.health == 0:
                            enemy.kill()
                            self.score += 1
                    elif (
                        isinstance(hz, LavaZone)
                        and now - self.last_hazard_damage >= hz.interval
                    ):
                        enemy.take_damage(hz.damage)
                        self.last_hazard_damage = now
                    enemy.update(self.ground_y, now)
                self.ally_manager.update(self.player, self.ground_y, now)
                self.projectiles.update()
                self.melee_attacks.update()
                self.healing_zones.update()
                self._handle_collisions()
                self.powerups.update()
                if now >= self.next_powerup_time:
                    x = self.width // 2
                    p = PowerUp(x, self.ground_y - 20, "heal")
                    self.powerups.add(p)
                    self.all_sprites.add(p)
                    self.next_powerup_time = now + 5000
                for zone in self.healing_zones:
                    if zone.rect.colliderect(self.player.rect):
                        self.player.health = min(
                            self.player.max_health,
                            self.player.health + zone.heal_rate,
                        )
                p = pygame.sprite.spritecollideany(self.player, self.powerups)
                if p:
                    if p.effect == "heal":
                        self.player.health = self.player.max_health
                    elif p.effect == "mana":
                        self.player.mana = self.player.max_mana
                    p.kill()
                for proj in list(self.projectiles):
                    if proj.rect.right < 0 or proj.rect.left > self.width:
                        proj.kill()
                if self.player.lives == 0:
                    self.final_time = (now - self.level_start_time) // 1000
                    if self.final_time > self.best_time:
                        self.best_time = self.final_time
                    if self.score > self.best_score:
                        self.best_score = self.score
                    self._set_state("game_over")
                    self.end_time = now
                    self.show_end_options = False
                    self.menu_index = 0
                    continue
                self.screen.fill((0, 0, 0))
                pygame.draw.rect(
                    self.screen,
                    (100, 100, 100),
                    pygame.Rect(
                        0, self.ground_y, self.width, self.height - self.ground_y
                    ),
                )
                self.all_sprites.draw(self.screen)
                self.player.draw_status(self.screen)
                if self.chat_manager.open:
                    chat_rect = pygame.Rect(10, self.height - 40, 300, 30)
                    pygame.draw.rect(self.screen, (50, 50, 50), chat_rect)
                    txt = self.menu_font.render(self.chat_input, True, (255, 255, 255))
                    self.screen.blit(txt, (chat_rect.x + 5, chat_rect.y + 5))
                elapsed = (now - self.level_start_time) // 1000
                if elapsed >= self.level_limit or len(self.enemies) == 0:
                    self.final_time = elapsed
                    if self.final_time > self.best_time:
                        self.best_time = self.final_time
                    if self.score > self.best_score:
                        self.best_score = self.score
                    self._set_state("victory")
                    self.end_time = now
                    self.show_end_options = False
                    self.menu_index = 0
                    continue
                timer_text = self.menu_font.render(
                    f"Time: {elapsed}", True, (255, 255, 255)
                )
                self.screen.blit(timer_text, (self.width - 120, 10))
                score_text = self.menu_font.render(
                    f"Score: {self.score}", True, (255, 255, 255)
                )
                self.screen.blit(score_text, (10, 10))

            self._poll_network()

            pygame.display.flip()
            self.clock.tick(60)
        save_settings(
            {
                "width": self.width,
                "height": self.height,
                "volume": self.volume,
                "best_time": self.best_time,
                "best_score": self.best_score,
                "show_fps": self.show_fps,
                "key_bindings": self.keybind_manager.to_dict(),
                "controller_bindings": self.controller_bindings,
            }
        )
        pygame.quit()


def main():
    """Entry point for running the game via `python -m hololive_coliseum`."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
