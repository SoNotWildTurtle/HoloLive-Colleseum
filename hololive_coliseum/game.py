import os
import pygame

from .player import Player, GuraPlayer
from .projectile import Projectile
from .melee_attack import MeleeAttack
from .gravity_zone import GravityZone
from .save_manager import load_settings, save_settings, wipe_saves


MENU_BG_COLOR = (0, 255, 255)  # cyan background
MENU_TEXT_COLOR = (255, 255, 255)  # white text


class Game:
    """Minimal game loop with a splash menu using pygame."""

    def __init__(self, width: int = 800, height: int = 600):
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        pygame.init()
        self.settings = load_settings()
        self.width = self.settings.get("width", width)
        self.height = self.settings.get("height", height)
        self.volume = self.settings.get("volume", 1.0)
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        try:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(self.volume)
        except pygame.error:
            pass
        default_keys = {
            "shoot": pygame.K_z,
            "melee": pygame.K_x,
            "jump": pygame.K_SPACE,
            "block": pygame.K_LSHIFT,
            "parry": pygame.K_c,
            "special": pygame.K_v,
        }
        self.key_bindings = self.settings.get("key_bindings", default_keys)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("HoloLive Coliseum")
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
            "Window Size",
            "Volume",
            "Wipe Saves",
            "Back",
        ]
        self.characters = ["Gawr Gura"]
        self.maps = ["Default"]
        self.chapters = ["Chapter 1"]
        self.selected_mode: str | None = None
        self.selected_character: str | None = None
        self.selected_map: str | None = None
        self.selected_chapter: str | None = None
        image_dir = os.path.join(os.path.dirname(__file__), '..', 'Images')

        def _load(name: str, size=(64, 64)) -> pygame.Surface:
            path = os.path.join(image_dir, name)
            if os.path.exists(path):
                return pygame.image.load(path).convert_alpha()
            surf = pygame.Surface(size)
            surf.fill((255, 255, 255))
            return surf

        self.character_images = {
            'Gawr Gura': _load('Gawr_Gura_right.png'),
        }
        self.map_images = {
            'Default': _load('map_default.png'),
        }
        self.chapter_images = {
            'Chapter 1': _load('chapter1.png'),
        }
        self.title_font = pygame.font.SysFont(None, 64)
        self.menu_font = pygame.font.SysFont(None, 32)

        # Simple stage with a single ground platform
        self.ground_y = self.height - 50
        player_image = os.path.join(image_dir, "Gawr_Gura_right.png")
        self.player = GuraPlayer(100, self.ground_y - 60, player_image)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.projectiles = pygame.sprite.Group()
        self.melee_attacks = pygame.sprite.Group()
        self.gravity_zones = pygame.sprite.Group()

        # Example low gravity zone in the middle of the stage
        zone_rect = pygame.Rect(self.width // 2 - 50, self.ground_y - 150, 100, 50)
        self.low_gravity_zone = GravityZone(zone_rect, 0.2)
        self.gravity_zones.add(self.low_gravity_zone)
        self.all_sprites.add(self.low_gravity_zone)

    def _draw_menu(self) -> None:
        """Render the splash menu screen."""
        self.screen.fill(MENU_BG_COLOR)
        title = self.title_font.render("HoloLive Coliseum", True, MENU_TEXT_COLOR)
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
        self._draw_option_menu("Select Character", self.characters)
        current = self.characters[self.menu_index]
        img = self.character_images[current]
        rect = img.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(img, rect)

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
        self._draw_option_menu("Settings", self.settings_options)

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
                        "char": self.characters,
                        "map": self.maps,
                        "chapter": self.chapters,
                    }[self.state]
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
                        pygame.mixer.music.set_volume(self.volume)
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
                            self.state = "solo_multi"
                            self.menu_index = 0
                        elif self.state == "solo_multi":
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
                            self.selected_character = choice
                            if self.selected_mode == "Story":
                                self.state = "chapter"
                            else:
                                self.state = "map"
                            self.menu_index = 0
                        elif self.state == "map":
                            self.selected_map = choice
                            self.state = "playing"
                        elif self.state == "chapter":
                            self.selected_chapter = choice
                            self.state = "playing"
                        elif self.state == "settings":
                            if choice == "Back":
                                self.state = "main_menu"
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
            else:
                keys = pygame.key.get_pressed()
                self.player.handle_input(keys, now, self.key_bindings)
                if keys[self.key_bindings.get("special", pygame.K_v)]:
                    proj = self.player.special_attack(now)
                    if proj:
                        self.projectiles.add(proj)
                        self.all_sprites.add(proj)
                if keys[self.key_bindings.get("shoot", pygame.K_z)]:
                    proj = self.player.shoot(now)
                    if proj:
                        self.projectiles.add(proj)
                        self.all_sprites.add(proj)
                if keys[self.key_bindings.get("melee", pygame.K_x)]:
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
                self.projectiles.update()
                self.melee_attacks.update()
                for proj in list(self.projectiles):
                    if proj.rect.right < 0 or proj.rect.left > self.width:
                        proj.kill()
                self.screen.fill((0, 0, 0))
                pygame.draw.rect(
                    self.screen,
                    (100, 100, 100),
                    pygame.Rect(0, self.ground_y, self.width, self.height - self.ground_y),
                )
                self.all_sprites.draw(self.screen)
                self.player.draw_status(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
        save_settings(
            {
                "width": self.width,
                "height": self.height,
                "volume": self.volume,
                "key_bindings": self.key_bindings,
            }
        )
        pygame.quit()


def main():
    """Entry point for running the game via `python -m hololive_coliseum`."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
