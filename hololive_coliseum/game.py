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
    Enemy,
)
from .projectile import Projectile, ExplodingProjectile
from .melee_attack import MeleeAttack
from .gravity_zone import GravityZone
from .hazards import SpikeTrap, IceZone
from .powerup import PowerUp
from .healing_zone import HealingZone
from .save_manager import load_settings, save_settings, wipe_saves
from .network import NetworkManager
from .node_registry import load_nodes
from .menus import MenuMixin, MENU_BG_COLOR, MENU_TEXT_COLOR
from .accounts import register_account, delete_account


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
        self.key_bindings = self.settings.get("key_bindings", default_keys)
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
        self.state = "splash"  # splash -> main_menu -> mode -> solo_multi -> mp_type -> char -> lobby -> map/chapter -> settings -> accounts -> playing
        self.menu_index = 0
        self.main_menu_options = ["New Game", "Settings", "Exit"]
        self.mode_options = ["Story", "Arena", "Custom", "Back"]
        self.solo_multi_options = ["Solo", "Multiplayer", "Back"]
        self.mp_type_options = ["Offline", "Online", "Back"]
        self.online_multiplayer = False
        self.settings_options = [
            "Key Bindings",
            "Controller Bindings",
            "Window Size",
            "Volume",
            "Wipe Saves",
            "Node Settings",
            "Accounts",
            "Back",
        ]
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
        self.node_options = ["Start Node", "Stop Node", "Back"]
        self.account_options = ["Register Account", "Delete Account", "Back"]
        self.account_id = "player"
        self.network_manager: NetworkManager | None = None
        self.node_hosting = False
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
        }
        self.map_images = {
            "Default": _load("map_default.png"),
        }
        self.chapter_images = {
            f"Chapter {i}": _load(f"chapter{i}.png") for i in range(1, 21)
        }
        self.title_font = pygame.font.SysFont(None, 64)
        self.menu_font = pygame.font.SysFont(None, 32)

        # Stage setup
        self.ground_y = self.height - 50
        self.next_powerup_time = 0
        self.last_enemy_damage = 0
        self.level_start_time = 0
        self.level_limit = 60  # seconds
        self._setup_level()

    def _setup_level(self) -> None:
        """Initialize or reset gameplay objects based on the chosen character."""
        image_dir = os.path.join(os.path.dirname(__file__), "..", "Images")
        if self.selected_character == "Watson Amelia":
            player_cls = WatsonPlayer
            img = os.path.join(image_dir, "Watson_Amelia_right.png")
        elif self.selected_character == "Ninomae Ina'nis":
            player_cls = InaPlayer
            img = os.path.join(image_dir, "Ninomae_Inanis_right.png")
        elif self.selected_character == "Takanashi Kiara":
            player_cls = KiaraPlayer
            img = os.path.join(image_dir, "Takanashi_Kiara_right.png")
        elif self.selected_character == "Mori Calliope":
            player_cls = CalliopePlayer
            img = os.path.join(image_dir, "Mori_Calliope_right.png")
        elif self.selected_character == "Ceres Fauna":
            player_cls = FaunaPlayer
            img = os.path.join(image_dir, "Ceres_Fauna_right.png")
        elif self.selected_character == "Ouro Kronii":
            player_cls = KroniiPlayer
            img = os.path.join(image_dir, "Ouro_Kronii_right.png")
        elif self.selected_character == "IRyS":
            player_cls = IRySPlayer
            img = os.path.join(image_dir, "IRyS_right.png")
        elif self.selected_character == "Nanashi Mumei":
            player_cls = MumeiPlayer
            img = os.path.join(image_dir, "Nanashi_Mumei_right.png")
        elif self.selected_character == "Hakos Baelz":
            player_cls = BaelzPlayer
            img = os.path.join(image_dir, "Hakos_Baelz_right.png")
        elif self.selected_character == "Shirakami Fubuki":
            player_cls = FubukiPlayer
            img = os.path.join(image_dir, "Shirakami_Fubuki_right.png")
        elif self.selected_character == "Sakura Miko":
            player_cls = MikoPlayer
            img = os.path.join(image_dir, "Sakura_Miko_right.png")
        elif self.selected_character == "Minato Aqua":
            player_cls = AquaPlayer
            img = os.path.join(image_dir, "Minato_Aqua_right.png")
        elif self.selected_character == "Usada Pekora":
            player_cls = PekoraPlayer
            img = os.path.join(image_dir, "Usada_Pekora_right.png")
        elif self.selected_character == "Houshou Marine":
            player_cls = MarinePlayer
            img = os.path.join(image_dir, "Houshou_Marine_right.png")
        elif self.selected_character == "Hoshimachi Suisei":
            player_cls = SuiseiPlayer
            img = os.path.join(image_dir, "Hoshimachi_Suisei_right.png")
        elif self.selected_character == "Nakiri Ayame":
            player_cls = AyamePlayer
            img = os.path.join(image_dir, "Nakiri_Ayame_right.png")
        elif self.selected_character == "Shirogane Noel":
            player_cls = NoelPlayer
            img = os.path.join(image_dir, "Shirogane_Noel_right.png")
        elif self.selected_character == "Shiranui Flare":
            player_cls = FlarePlayer
            img = os.path.join(image_dir, "Shiranui_Flare_right.png")
        elif self.selected_character == "Oozora Subaru":
            player_cls = SubaruPlayer
            img = os.path.join(image_dir, "Oozora_Subaru_right.png")
        else:
            player_cls = GuraPlayer
            img = os.path.join(image_dir, "Gawr_Gura_right.png")
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
        spike = SpikeTrap(pygame.Rect(self.width // 3, self.ground_y - 20, 40, 20))
        ice = IceZone(pygame.Rect(self.width // 2 + 80, self.ground_y - 20, 60, 20))
        self.hazards.add(spike, ice)
        self.all_sprites.add(spike, ice)

    def _cycle_volume(self) -> None:
        """Cycle master volume between 0%, 50% and 100%."""
        steps = [0.0, 0.5, 1.0]
        current = min(steps, key=lambda v: abs(v - self.volume))
        idx = steps.index(current)
        self.volume = steps[(idx + 1) % len(steps)]
        if self.mixer_ready:
            pygame.mixer.music.set_volume(self.volume)

    def execute_account_option(self, option: str) -> None:
        """Handle register/delete actions for tests and menus."""
        if option == "Register Account":
            register_account(self.account_id, "user", "PUBKEY")
        elif option == "Delete Account":
            delete_account(self.account_id)

    def start_node(self) -> None:
        """Begin hosting a blockchain node."""
        if self.network_manager is None:
            self.network_manager = NetworkManager(host=True)
            self.network_manager.broadcast_announce(load_nodes())
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
                        enemy.velocity.x *= 0.5
                        enemy.velocity.y *= 0.5
                        enemy.take_damage(5)
                    elif getattr(proj, "slow", False):
                        enemy.velocity.x *= 0.5
                        enemy.take_damage(5)
                    else:
                        enemy.take_damage(10)
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
                    self.state = "main_menu"
                    self.menu_index = 0
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
                    }
                    and event.type == pygame.KEYDOWN
                ):
                    options = {
                        "main_menu": self.main_menu_options,
                        "mode": self.mode_options,
                        "solo_multi": self.solo_multi_options,
                        "mp_type": self.mp_type_options,
                        "settings": self.settings_options,
                        "node_settings": self.node_options,
                        "accounts": self.account_options,
                        "key_bindings": self.key_options,
                        "controller_bindings": self.controller_options,
                        "char": self.character_menu_options,
                        "map": self.map_menu_options,
                        "chapter": self.chapter_menu_options,
                        "lobby": self.lobby_options,
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
                        self.menu_index = (self.menu_index - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        self.menu_index = (self.menu_index + 1) % len(options)
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
                        self.state = "rebind"
                    elif (
                        self.state == "controller_bindings"
                        and options[self.menu_index] != "Back"
                        and event.key in (pygame.K_RETURN, pygame.K_SPACE)
                    ):
                        self.rebind_action = options[self.menu_index]
                        self.state = "rebind_controller"
                    elif (
                        self.state == "key_bindings"
                        and options[self.menu_index] == "Back"
                        and event.key in (pygame.K_RETURN, pygame.K_SPACE)
                    ):
                        self.state = "settings"
                        self.menu_index = 0
                    elif (
                        self.state == "controller_bindings"
                        and options[self.menu_index] == "Back"
                        and event.key in (pygame.K_RETURN, pygame.K_SPACE)
                    ):
                        self.state = "settings"
                        self.menu_index = 0
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        choice = options[self.menu_index]
                        if self.state == "main_menu":
                            if choice == "New Game":
                                self.state = "mode"
                                self.menu_index = 0
                            elif choice == "Settings":
                                self.state = "settings"
                                self.menu_index = 0
                            elif choice == "Exit":
                                self.running = False
                        elif self.state == "mode":
                            if choice == "Back":
                                self.state = "main_menu"
                                self.menu_index = 0
                            else:
                                self.selected_mode = choice
                                self.human_players = 1
                                self.ai_players = 0
                                self.state = "solo_multi"
                                self.menu_index = 0
                        elif self.state == "solo_multi":
                            if choice == "Back":
                                self.state = "mode"
                                self.menu_index = 0
                            else:
                                self.multiplayer = choice == "Multiplayer"
                                if choice == "Solo":
                                    self.state = "char"
                                else:
                                    self.state = "mp_type"
                                self.menu_index = 0
                        elif self.state == "mp_type":
                            if choice == "Back":
                                self.state = "solo_multi"
                                self.menu_index = 0
                            else:
                                self.online_multiplayer = choice == "Online"
                                self.state = "char"
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
                                    self.state = "lobby"
                                elif self.selected_mode == "Story":
                                    self.state = "chapter"
                                else:
                                    self.state = "map"
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
                                self.state = "char"
                                self.menu_index = 0
                            elif choice == "Start Game":
                                if self.selected_mode == "Story":
                                    self.state = "chapter"
                                else:
                                    self.state = "map"
                                self.menu_index = 0
                        elif self.state == "map":
                            if choice == "Back":
                                if self.multiplayer:
                                    self.state = "lobby"
                                else:
                                    self.state = "char"
                                self.menu_index = 0
                            else:
                                self.selected_map = choice
                                self._setup_level()
                                self.state = "playing"
                                self.level_start_time = pygame.time.get_ticks()
                        elif self.state == "chapter":
                            if choice == "Back":
                                if self.multiplayer:
                                    self.state = "lobby"
                                else:
                                    self.state = "char"
                                self.menu_index = 0
                            else:
                                self.selected_chapter = choice
                                self._setup_level()
                                self.state = "playing"
                                self.level_start_time = pygame.time.get_ticks()
                        elif self.state == "settings":
                            if choice == "Back":
                                self.state = "main_menu"
                                self.menu_index = 0
                            elif choice == "Key Bindings":
                                self.state = "key_bindings"
                                self.menu_index = 0
                            elif choice == "Controller Bindings":
                                self.state = "controller_bindings"
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
                            elif choice == "Wipe Saves":
                                wipe_saves()
                            elif choice == "Node Settings":
                                self.state = "node_settings"
                                self.menu_index = 0
                            elif choice == "Accounts":
                                self.state = "accounts"
                                self.menu_index = 0
                        elif self.state == "node_settings":
                            if choice == "Back":
                                self.state = "settings"
                                self.menu_index = 0
                            elif choice == "Start Node":
                                self.start_node()
                            elif choice == "Stop Node":
                                self.stop_node()
                        elif self.state == "accounts":
                            if choice == "Back":
                                self.state = "settings"
                                self.menu_index = 0
                            elif choice == "Register Account":
                                self.execute_account_option("Register Account")
                            elif choice == "Delete Account":
                                self.execute_account_option("Delete Account")
                elif self.state == "rebind" and event.type == pygame.KEYDOWN:
                    self.key_bindings[self.rebind_action] = event.key
                    self.state = "key_bindings"
                elif (
                    self.state == "rebind_controller"
                    and event.type == pygame.JOYBUTTONDOWN
                ):
                    self.controller_bindings[self.rebind_action] = event.button
                    self.state = "controller_bindings"
            now = pygame.time.get_ticks()

            if self.state == "splash":
                self._draw_menu()
            elif self.state == "main_menu":
                self._draw_option_menu("Main Menu", self.main_menu_options)
            elif self.state == "mode":
                self._draw_option_menu("Game Type", self.mode_options)
            elif self.state == "solo_multi":
                self._draw_option_menu("Players", self.solo_multi_options)
            elif self.state == "mp_type":
                self._draw_option_menu("Multiplayer", self.mp_type_options)
            elif self.state == "char":
                self._draw_character_menu()
            elif self.state == "map":
                self._draw_map_menu()
            elif self.state == "chapter":
                self._draw_chapter_menu()
            elif self.state == "lobby":
                self._draw_lobby_menu()
            elif self.state == "settings":
                self._draw_settings_menu()
            elif self.state == "key_bindings":
                self._draw_key_bindings_menu()
            elif self.state == "controller_bindings":
                self._draw_controller_bindings_menu()
            elif self.state == "rebind":
                self._draw_rebind_prompt()
            elif self.state == "rebind_controller":
                self._draw_rebind_controller_prompt()
            elif self.state == "node_settings":
                self._draw_node_menu()
            elif self.state == "accounts":
                self._draw_accounts_menu()
            else:
                keys = pygame.key.get_pressed()

                def action_pressed(action: str) -> bool:
                    key = self.key_bindings.get(action)
                    if key is not None and keys[key]:
                        return True
                    for joy in self.joysticks:
                        btn = self.controller_bindings.get(action)
                        if btn is not None and joy.get_button(btn):
                            return True
                    return False

                self.player.handle_input(keys, now, self.key_bindings, action_pressed)
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
                    if (
                        isinstance(hazard, SpikeTrap)
                        and now - self.last_hazard_damage >= 500
                    ):
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
                for enemy in self.enemies:
                    proj, melee = enemy.handle_ai(
                        self.player, now, self.hazards, self.projectiles
                    )
                    if proj:
                        self.projectiles.add(proj)
                        self.all_sprites.add(proj)
                    if melee:
                        self.melee_attacks.add(melee)
                        self.all_sprites.add(melee)
                    zone = pygame.sprite.spritecollideany(enemy, self.gravity_zones)
                    if zone:
                        enemy.set_gravity_multiplier(zone.multiplier)
                    else:
                        enemy.set_gravity_multiplier(1.0)
                    hz = pygame.sprite.spritecollideany(enemy, self.hazards)
                    if isinstance(hz, SpikeTrap):
                        enemy.take_damage(hz.damage)
                    enemy.update(self.ground_y, now)
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
                    self.state = "main_menu"
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
                elapsed = (now - self.level_start_time) // 1000
                timer_text = self.menu_font.render(
                    f"Time: {elapsed}", True, (255, 255, 255)
                )
                self.screen.blit(timer_text, (self.width - 120, 10))

            self._poll_network()

            pygame.display.flip()
            self.clock.tick(60)
        save_settings(
            {
                "width": self.width,
                "height": self.height,
                "volume": self.volume,
                "key_bindings": self.key_bindings,
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
