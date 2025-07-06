import os
import pygame

from .player import Player


MENU_BG_COLOR = (0, 255, 255)  # cyan background
MENU_TEXT_COLOR = (255, 255, 255)  # white text


class Game:
    """Minimal game loop with a splash menu using pygame."""

    def __init__(self, width: int = 800, height: int = 600):
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("HoloLive Coliseum")
        self.clock = pygame.time.Clock()
        self.running = False
        self.in_menu = True
        self.title_font = pygame.font.SysFont(None, 64)
        self.menu_font = pygame.font.SysFont(None, 32)

        # Simple stage with a single ground platform
        self.ground_y = self.height - 50
        self.player = Player(100, self.ground_y - 60)
        self.all_sprites = pygame.sprite.Group(self.player)

    def _draw_menu(self) -> None:
        """Render the splash menu screen."""
        self.screen.fill(MENU_BG_COLOR)
        title = self.title_font.render("HoloLive Coliseum", True, MENU_TEXT_COLOR)
        prompt = self.menu_font.render("Press any key to start", True, MENU_TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 3)))
        self.screen.blit(prompt, prompt.get_rect(center=(self.width // 2, self.height // 2)))

    def run(self):
        """Start the main game loop."""
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.in_menu and event.type == pygame.KEYDOWN:
                    self.in_menu = False

            if self.in_menu:
                self._draw_menu()
            else:
                keys = pygame.key.get_pressed()
                self.player.handle_input(keys)
                self.player.update(self.ground_y)

                self.screen.fill((0, 0, 0))
                pygame.draw.rect(
                    self.screen,
                    (100, 100, 100),
                    pygame.Rect(0, self.ground_y, self.width, self.height - self.ground_y),
                )
                self.all_sprites.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


def main():
    """Entry point for running the game via `python -m hololive_coliseum`."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
