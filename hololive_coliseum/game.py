import os
import pygame

from .player import Player, GuraPlayer, WatsonPlayer, Enemy
from .projectile import Projectile, ExplodingProjectile
from .melee_attack import MeleeAttack
from .gravity_zone import GravityZone
from .powerup import PowerUp
from .save_manager import load_settings, save_settings, wipe_saves


MENU_BG_COLOR = (0, 255, 255)  # cyan background
MENU_TEXT_COLOR = (255, 255, 255)  # white text


class Game:
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
            "special": pygame.K_v,
        }
        self.key_bindings = self.settings.get("key_bindings", default_keys)
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        default_controller = {
            "shoot": 0,
            "melee": 1,
            "jump": 2,
            "block": 4,
            "parry": 5,
            "special": 3,
        }
        self.controller_bindings = self.settings.get("controller_bindings", default_controller)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Hololive Coliseum")
        self.clock = pygame.time.Clock()
        self.running = False
        self.state = "splash"  # splash -> main_menu -> mode -> solo_multi -> mp_type -> char -> map/chapter -> settings -> playing
        self.menu_index = 0
        self.main_menu_options = ["New Game", "Settings", "Exit"]
        self.mode_options = ["Story", "Arena", "Custom"]
        self.solo_multi_options = ["Solo", "Multiplayer"]
        self.mp_type_options = ["Offline", "Online"]
        self.online_multiplayer = False
        self.settings_options = [
            "Key Bindings",
            "Controller Bindings",
            "Window Size",
            "Volume",
            "Wipe Saves",
            "Back",
        ]
        self.key_options = [
            "jump",
            "shoot",
            "melee",
            "block",
            "parry",
            "special",
            "Back",
        ]
        self.controller_options = list(self.key_options)
        self.rebind_action: str | None = None
        self.characters = ["Gawr Gura", "Watson Amelia"]
        self.maps = ["Default"]
        self.chapters = [f"Chapter {i}" for i in range(1, 21)]
        self.character_menu_options = self.characters + ["Add AI Player", "Continue"]
        self.human_players = 1
        self.ai_players = 0
        self.multiplayer = False
        self.selected_mode: str | None = None
        self.selected_character: str | None = None
        self.selected_map: str | None = None
        self.selected_chapter: str | None = None
        image_dir = os.path.join(os.path.dirname(__file__), '..', 'Images')

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
            'Gawr Gura': _load('Gawr_Gura_right.png'),
            'Watson Amelia': _load('Watson_Amelia_right.png'),
        }
        self.map_images = {
            'Default': _load('map_default.png'),
        }
        self.chapter_images = {
            f'Chapter {i}': _load(f'chapter{i}.png') for i in range(1, 21)
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
        image_dir = os.path.join(os.path.dirname(__file__), '..', 'Images')
        if self.selected_character == 'Watson Amelia':
            player_cls = WatsonPlayer
            img = os.path.join(image_dir, 'Watson_Amelia_right.png')
        else:
            player_cls = GuraPlayer
            img = os.path.join(image_dir, 'Gawr_Gura_right.png')
        self.player = player_cls(100, self.ground_y - 60, img)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.projectiles = pygame.sprite.Group()
        self.melee_attacks = pygame.sprite.Group()
        self.gravity_zones = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        # Reset timers when starting a new level
        self.next_powerup_time = 0
        self.last_enemy_damage = 0
        for i in range(self.ai_players):
            e = Enemy(300 + i * 60, self.ground_y - 60, os.path.join(image_dir, "enemy_right.png"))
            self.enemies.add(e)
            self.all_sprites.add(e)

        zone_rect = pygame.Rect(self.width // 2 - 50, self.ground_y - 150, 100, 50)
        self.low_gravity_zone = GravityZone(zone_rect, 0.2)
        self.gravity_zones.add(self.low_gravity_zone)
        self.all_sprites.add(self.low_gravity_zone)

    def _draw_menu(self) -> None:
        """Render the splash menu screen."""
        self.screen.fill(MENU_BG_COLOR)
        title = self.title_font.render("Hololive Coliseum", True, MENU_TEXT_COLOR)
        prompt = self.menu_font.render("Press any key to start", True, MENU_TEXT_COLOR)
        self.screen.blit(
            title, title.get_rect(center=(self.width // 2, self.height // 3))
        )
        self.screen.blit(
            prompt, prompt.get_rect(center=(self.width // 2, self.height // 2))
        )

    def _draw_option_menu(self, title: str, options: list[str]) -> None:
        """Generic menu drawing helper."""
        self.screen.fill(MENU_BG_COLOR)
        t = self.title_font.render(title, True, MENU_TEXT_COLOR)
        self.screen.blit(t, t.get_rect(center=(self.width // 2, self.height // 4)))
        for i, opt in enumerate(options):
            color = MENU_TEXT_COLOR if i == self.menu_index else (50, 50, 50)
            text = self.menu_font.render(opt, True, color)
            rect = text.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
            self.screen.blit(text, rect)

    def _draw_character_menu(self) -> None:
        self._draw_option_menu("Select Character", self.character_menu_options)
        if self.menu_index < len(self.characters):
            current = self.characters[self.menu_index]
            img = self.character_images[current]
            rect = img.get_rect(center=(self.width // 2, self.height // 2 - 100))
            self.screen.blit(img, rect)
        info = f"AI Players: {self.ai_players}"
        if self.multiplayer and not self.online_multiplayer:
            info += f" | Players Joined: {self.human_players}"
        text = self.menu_font.render(info, True, MENU_TEXT_COLOR)
        self.screen.blit(text, text.get_rect(center=(self.width // 2, self.height - 40)))
        if self.multiplayer and not self.online_multiplayer:
            prompt = self.menu_font.render("Press J to join", True, MENU_TEXT_COLOR)
            self.screen.blit(prompt, prompt.get_rect(center=(self.width // 2, self.height - 20)))

    def _draw_map_menu(self) -> None:
        self._draw_option_menu("Select Map", self.maps)
        current = self.maps[self.menu_index]
        img = self.map_images[current]
        rect = img.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(img, rect)

    def _draw_chapter_menu(self) -> None:
        self._draw_option_menu("Select Chapter", self.chapters)
        current = self.chapters[self.menu_index]
        img = self.chapter_images[current]
        rect = img.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(img, rect)

    def _draw_settings_menu(self) -> None:
        """Display the settings options."""
        self.screen.fill(MENU_BG_COLOR)
        t = self.title_font.render("Settings", True, MENU_TEXT_COLOR)
        self.screen.blit(t, t.get_rect(center=(self.width // 2, self.height // 4)))
        for i, opt in enumerate(self.settings_options):
            label = opt
            if opt == "Volume":
                label = f"Volume: {int(self.volume * 100)}%"
            color = MENU_TEXT_COLOR if i == self.menu_index else (50, 50, 50)
            text = self.menu_font.render(label, True, color)
            rect = text.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
            self.screen.blit(text, rect)

    def _draw_key_bindings_menu(self) -> None:
        """Show current key bindings and allow selection for rebinding."""
        self.screen.fill(MENU_BG_COLOR)
        t = self.title_font.render("Key Bindings", True, MENU_TEXT_COLOR)
        self.screen.blit(t, t.get_rect(center=(self.width // 2, self.height // 4)))
        for i, action in enumerate(self.key_options):
            if action == "Back":
                label = "Back"
            else:
                key_name = pygame.key.name(self.key_bindings.get(action, 0))
                label = f"{action.title()}: {key_name}"
            color = MENU_TEXT_COLOR if i == self.menu_index else (50, 50, 50)
            text = self.menu_font.render(label, True, color)
            rect = text.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
            self.screen.blit(text, rect)

    def _draw_controller_bindings_menu(self) -> None:
        """Display controller button mappings."""
        self.screen.fill(MENU_BG_COLOR)
        t = self.title_font.render("Controller Bindings", True, MENU_TEXT_COLOR)
        self.screen.blit(t, t.get_rect(center=(self.width // 2, self.height // 4)))
        for i, action in enumerate(self.controller_options):
            if action == "Back":
                label = "Back"
            else:
                label = f"{action.title()}: {self.controller_bindings.get(action, 0)}"
            color = MENU_TEXT_COLOR if i == self.menu_index else (50, 50, 50)
            text = self.menu_font.render(label, True, color)
            rect = text.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
            self.screen.blit(text, rect)

    def _draw_rebind_prompt(self) -> None:
        self.screen.fill(MENU_BG_COLOR)
        prompt = self.menu_font.render(
            f"Press a key for {self.rebind_action.title()}", True, MENU_TEXT_COLOR
        )
        self.screen.blit(prompt, prompt.get_rect(center=(self.width // 2, self.height // 2)))

    def _draw_rebind_controller_prompt(self) -> None:
        self.screen.fill(MENU_BG_COLOR)
        prompt = self.menu_font.render(
            f"Press a button for {self.rebind_action.title()}", True, MENU_TEXT_COLOR
        )
        self.screen.blit(prompt, prompt.get_rect(center=(self.width // 2, self.height // 2)))

    def _handle_collisions(self) -> None:
        """Handle combat collisions between attacks and sprites."""
        now = pygame.time.get_ticks()
        for proj in list(self.projectiles):
            hits = pygame.sprite.spritecollide(proj, self.enemies, False)
            if hits:
                for enemy in hits:
                    enemy.take_damage(10)
                proj.kill()
        for attack in list(self.melee_attacks):
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
                elif self.state in {
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
                } and event.type == pygame.KEYDOWN:
                    options = {
                        "main_menu": self.main_menu_options,
                        "mode": self.mode_options,
                        "solo_multi": self.solo_multi_options,
                        "mp_type": self.mp_type_options,
                        "settings": self.settings_options,
                        "key_bindings": self.key_options,
                        "controller_bindings": self.controller_options,
                        "char": self.character_menu_options,
                        "map": self.maps,
                        "chapter": self.chapters,
                    }[self.state]
                    if (
                        self.state == "char"
                        and event.key == pygame.K_j
                        and self.multiplayer
                        and not self.online_multiplayer
                    ):
                        if self.human_players < 4:
                            self.human_players += 1
                        continue
                    if event.key == pygame.K_UP:
                        self.menu_index = (self.menu_index - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        self.menu_index = (self.menu_index + 1) % len(options)
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
                            self.selected_mode = choice
                            self.human_players = 1
                            self.ai_players = 0
                            self.state = "solo_multi"
                            self.menu_index = 0
                        elif self.state == "solo_multi":
                            self.multiplayer = choice == "Multiplayer"
                            if choice == "Solo":
                                self.state = "char"
                            else:
                                self.state = "mp_type"
                            self.menu_index = 0
                        elif self.state == "mp_type":
                            self.online_multiplayer = choice == "Online"
                            self.state = "char"
                            self.menu_index = 0
                        elif self.state == "char":
                            if choice == "Add AI Player":
                                if self.ai_players < 4 - self.human_players:
                                    self.ai_players += 1
                            elif choice == "Continue":
                                if self.selected_character is None and self.characters:
                                    self.selected_character = self.characters[0]
                                if self.selected_mode == "Story":
                                    self.state = "chapter"
                                else:
                                    self.state = "map"
                                self.menu_index = 0
                            else:
                                self.selected_character = choice
                        elif self.state == "map":
                            self.selected_map = choice
                            self._setup_level()
                            self.state = "playing"
                            self.level_start_time = pygame.time.get_ticks()
                        elif self.state == "chapter":
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
                                self.screen = pygame.display.set_mode((self.width, self.height))
                            elif choice == "Volume":
                                pass
                            elif choice == "Wipe Saves":
                                wipe_saves()
                elif self.state == "rebind" and event.type == pygame.KEYDOWN:
                    self.key_bindings[self.rebind_action] = event.key
                    self.state = "key_bindings"
                elif self.state == "rebind_controller" and event.type == pygame.JOYBUTTONDOWN:
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
                    if proj:
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
                self.player.update(self.ground_y, now)
                for enemy in self.enemies:
                    enemy.handle_ai(self.player, now)
                    enemy.update(self.ground_y, now)
                self.projectiles.update()
                self.melee_attacks.update()
                self._handle_collisions()
                self.powerups.update()
                if now >= self.next_powerup_time:
                    x = self.width // 2
                    p = PowerUp(x, self.ground_y - 20, "heal")
                    self.powerups.add(p)
                    self.all_sprites.add(p)
                    self.next_powerup_time = now + 5000
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
                    pygame.Rect(0, self.ground_y, self.width, self.height - self.ground_y),
                )
                self.all_sprites.draw(self.screen)
                self.player.draw_status(self.screen)
                elapsed = (now - self.level_start_time) // 1000
                timer_text = self.menu_font.render(f"Time: {elapsed}", True, (255, 255, 255))
                self.screen.blit(timer_text, (self.width - 120, 10))

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
