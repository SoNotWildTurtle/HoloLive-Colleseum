"""Menu rendering helpers used by :class:`~hololive_coliseum.game.Game`."""

from __future__ import annotations

import pygame

MENU_BG_COLOR = (0, 255, 255)  # cyan background
MENU_TEXT_COLOR = (255, 255, 255)  # white text
MENU_BORDER_COLOR = (0, 200, 200)  # teal border


class MenuMixin:
    """Provides drawing helpers for the game's various menus."""

    def _draw_border(self) -> None:
        """Draw a teal border without covering the corners used by tests."""
        rect = self.screen.get_rect().inflate(-10, -10)
        pygame.draw.rect(self.screen, MENU_BORDER_COLOR, rect, 4)

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
        self._draw_border()

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
        self._draw_border()

    def _draw_character_menu(self) -> None:
        self.screen.fill(MENU_BG_COLOR)
        title = self.title_font.render("Select Character", True, MENU_TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 40)))
        cols = 5
        size = 64
        margin = 20
        start_x = (self.width - (cols * size + (cols - 1) * margin)) // 2
        start_y = 80
        for idx, name in enumerate(self.characters):
            row = idx // cols
            col = idx % cols
            x = start_x + col * (size + margin)
            y = start_y + row * (size + margin)
            img = self.character_images[name]
            rect = img.get_rect(topleft=(x, y))
            self.screen.blit(img, rect)
            if idx == self.menu_index:
                pygame.draw.rect(self.screen, (255, 255, 0), rect, 2)
        option_y = (
            start_y + ((len(self.characters) - 1) // cols + 1) * (size + margin) + 20
        )
        options = ["Add AI Player", "Difficulty", "Continue", "Back"]
        for i, opt in enumerate(options):
            idx = len(self.characters) + i
            label = opt
            if opt == "Difficulty":
                label = f"Difficulty: {self.difficulty_levels[self.difficulty_index]}"
            color = MENU_TEXT_COLOR if idx == self.menu_index else (50, 50, 50)
            text = self.menu_font.render(label, True, color)
            rect = text.get_rect(center=(self.width // 2, option_y + i * 40))
            self.screen.blit(text, rect)
        info = f"AI Players: {self.ai_players}"
        if self.multiplayer and not self.online_multiplayer:
            info += f" | Players Joined: {self.human_players}"
        text = self.menu_font.render(info, True, MENU_TEXT_COLOR)
        self.screen.blit(
            text, text.get_rect(center=(self.width // 2, self.height - 40))
        )
        if self.multiplayer and not self.online_multiplayer:
            prompt = self.menu_font.render("Press J to join", True, MENU_TEXT_COLOR)
            self.screen.blit(
                prompt, prompt.get_rect(center=(self.width // 2, self.height - 20))
            )
        self._draw_border()

    def _draw_map_menu(self) -> None:
        self.screen.fill(MENU_BG_COLOR)
        title = self.title_font.render("Select Map", True, MENU_TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 40)))
        cols = 5
        size = 64
        margin = 20
        start_x = (self.width - (cols * size + (cols - 1) * margin)) // 2
        start_y = 80
        for idx, name in enumerate(self.maps):
            row = idx // cols
            col = idx % cols
            x = start_x + col * (size + margin)
            y = start_y + row * (size + margin)
            img = self.map_images[name]
            rect = img.get_rect(topleft=(x, y))
            self.screen.blit(img, rect)
            if idx == self.menu_index:
                pygame.draw.rect(self.screen, (255, 255, 0), rect, 2)
        back_idx = len(self.maps)
        text = self.menu_font.render(
            "Back",
            True,
            MENU_TEXT_COLOR if self.menu_index == back_idx else (50, 50, 50),
        )
        rect = text.get_rect(
            center=(
                self.width // 2,
                start_y + ((len(self.maps) - 1) // cols + 1) * (size + margin) + 20,
            )
        )
        self.screen.blit(text, rect)
        self._draw_border()

    def _draw_chapter_menu(self) -> None:
        self.screen.fill(MENU_BG_COLOR)
        title = self.title_font.render("Select Chapter", True, MENU_TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 40)))
        cols = 5
        size = 64
        margin = 20
        start_x = (self.width - (cols * size + (cols - 1) * margin)) // 2
        start_y = 80
        for idx, name in enumerate(self.chapters):
            row = idx // cols
            col = idx % cols
            x = start_x + col * (size + margin)
            y = start_y + row * (size + margin)
            img = self.chapter_images[name]
            rect = img.get_rect(topleft=(x, y))
            self.screen.blit(img, rect)
            if idx == self.menu_index:
                pygame.draw.rect(self.screen, (255, 255, 0), rect, 2)
        back_idx = len(self.chapters)
        text = self.menu_font.render(
            "Back",
            True,
            MENU_TEXT_COLOR if self.menu_index == back_idx else (50, 50, 50),
        )
        rect = text.get_rect(
            center=(
                self.width // 2,
                start_y + ((len(self.chapters) - 1) // cols + 1) * (size + margin) + 20,
            )
        )
        self.screen.blit(text, rect)
        self._draw_border()

    def _draw_settings_menu(self) -> None:
        """Display the settings options."""
        self.screen.fill(MENU_BG_COLOR)
        t = self.title_font.render("Settings", True, MENU_TEXT_COLOR)
        self.screen.blit(t, t.get_rect(center=(self.width // 2, self.height // 4)))
        for i, opt in enumerate(self.settings_options):
            label = opt
            if opt == "Volume":
                label = f"Volume: {int(self.volume * 100)}%"
            elif opt == "Show FPS":
                label = f"Show FPS: {'On' if self.show_fps else 'Off'}"
            color = MENU_TEXT_COLOR if i == self.menu_index else (50, 50, 50)
            text = self.menu_font.render(label, True, color)
            rect = text.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
            self.screen.blit(text, rect)
        self._draw_border()

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
        self._draw_border()

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
        self._draw_border()

    def _draw_rebind_prompt(self) -> None:
        self.screen.fill(MENU_BG_COLOR)
        prompt = self.menu_font.render(
            f"Press a key for {self.rebind_action.title()}", True, MENU_TEXT_COLOR
        )
        self.screen.blit(
            prompt, prompt.get_rect(center=(self.width // 2, self.height // 2))
        )
        self._draw_border()

    def _draw_rebind_controller_prompt(self) -> None:
        self.screen.fill(MENU_BG_COLOR)
        prompt = self.menu_font.render(
            f"Press a button for {self.rebind_action.title()}", True, MENU_TEXT_COLOR
        )
        self.screen.blit(
            prompt, prompt.get_rect(center=(self.width // 2, self.height // 2))
        )
        self._draw_border()

    def _draw_node_menu(self) -> None:
        """Display node hosting options."""
        self.screen.fill(MENU_BG_COLOR)
        t = self.title_font.render("Node Settings", True, MENU_TEXT_COLOR)
        self.screen.blit(t, t.get_rect(center=(self.width // 2, self.height // 4)))
        for i, opt in enumerate(self.node_options):
            color = MENU_TEXT_COLOR if i == self.menu_index else (50, 50, 50)
            label = opt
            if opt == "Start Node" and self.node_hosting:
                label = "Start Node (running)"
            if opt == "Latency Helper" and self.latency_helper:
                label = "Latency Helper (on)"
            text = self.menu_font.render(label, True, color)
            rect = text.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
            self.screen.blit(text, rect)
        self._draw_border()

    def _draw_accounts_menu(self) -> None:
        """Display simple account management options."""
        self.screen.fill(MENU_BG_COLOR)
        t = self.title_font.render("Accounts", True, MENU_TEXT_COLOR)
        self.screen.blit(t, t.get_rect(center=(self.width // 2, self.height // 4)))
        for i, opt in enumerate(self.account_options):
            color = MENU_TEXT_COLOR if i == self.menu_index else (50, 50, 50)
            text = self.menu_font.render(opt, True, color)
            rect = text.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
            self.screen.blit(text, rect)
        self._draw_border()

    def _draw_lobby_menu(self) -> None:
        """Show current players before starting multiplayer."""
        self.screen.fill(MENU_BG_COLOR)
        title = self.title_font.render("Lobby", True, MENU_TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 40)))
        for i, name in enumerate(self.player_names):
            text = self.menu_font.render(name, True, MENU_TEXT_COLOR)
            self.screen.blit(
                text, text.get_rect(center=(self.width // 2, 100 + i * 30))
            )
        for i, opt in enumerate(self.lobby_options):
            idx = len(self.player_names) + i
            color = MENU_TEXT_COLOR if self.menu_index == idx else (50, 50, 50)
            text = self.menu_font.render(opt, True, color)
            self.screen.blit(
                text, text.get_rect(center=(self.width // 2, self.height - 80 + i * 40))
            )
        self._draw_border()

    def _draw_pause_menu(self) -> None:
        """Display a simple pause menu."""
        self._draw_option_menu("Paused", self.pause_options)

    def _draw_game_over_menu(self) -> None:
        """Display results after the player loses all lives."""
        self.screen.fill(MENU_BG_COLOR)
        title = self.title_font.render("Game Over", True, MENU_TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 3)))
        time_text = self.menu_font.render(f"Time: {self.final_time}s", True, MENU_TEXT_COLOR)
        self.screen.blit(time_text, time_text.get_rect(center=(self.width // 2, self.height // 2 - 20)))
        best_text = self.menu_font.render(
            f"Best: {self.best_time}s", True, MENU_TEXT_COLOR
        )
        self.screen.blit(
            best_text, best_text.get_rect(center=(self.width // 2, self.height // 2 + 10))
        )
        high_score_text = self.menu_font.render(
            f"High Score: {self.best_score}", True, MENU_TEXT_COLOR
        )
        self.screen.blit(
            high_score_text, high_score_text.get_rect(center=(self.width // 2, self.height // 2 + 40))
        )
        score_text = self.menu_font.render(
            f"Score: {self.score}", True, MENU_TEXT_COLOR
        )
        self.screen.blit(
            score_text, score_text.get_rect(center=(self.width // 2, self.height // 2 + 70))
        )
        if self.show_end_options:
            for i, opt in enumerate(self.game_over_options):
                color = MENU_TEXT_COLOR if i == self.menu_index else (50, 50, 50)
                text = self.menu_font.render(opt, True, color)
                rect = text.get_rect(center=(self.width // 2, self.height // 2 + 80 + 40 * i))
                self.screen.blit(text, rect)
        self._draw_border()

    def _draw_victory_menu(self) -> None:
        """Display results after clearing the stage."""
        self.screen.fill(MENU_BG_COLOR)
        title = self.title_font.render("Victory!", True, MENU_TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 3)))
        time_text = self.menu_font.render(f"Time: {self.final_time}s", True, MENU_TEXT_COLOR)
        self.screen.blit(time_text, time_text.get_rect(center=(self.width // 2, self.height // 2 - 20)))
        best_text = self.menu_font.render(
            f"Best: {self.best_time}s", True, MENU_TEXT_COLOR
        )
        self.screen.blit(
            best_text, best_text.get_rect(center=(self.width // 2, self.height // 2 + 10))
        )
        high_score_text = self.menu_font.render(
            f"High Score: {self.best_score}", True, MENU_TEXT_COLOR
        )
        self.screen.blit(
            high_score_text, high_score_text.get_rect(center=(self.width // 2, self.height // 2 + 40))
        )
        score_text = self.menu_font.render(
            f"Score: {self.score}", True, MENU_TEXT_COLOR
        )
        self.screen.blit(
            score_text, score_text.get_rect(center=(self.width // 2, self.height // 2 + 70))
        )
        if self.show_end_options:
            for i, opt in enumerate(self.victory_options):
                color = MENU_TEXT_COLOR if i == self.menu_index else (50, 50, 50)
                text = self.menu_font.render(opt, True, color)
                rect = text.get_rect(center=(self.width // 2, self.height // 2 + 80 + 40 * i))
                self.screen.blit(text, rect)
        self._draw_border()

    def _draw_how_to_play(self) -> None:
        """Show basic controls and objective."""
        self.screen.fill(MENU_BG_COLOR)
        title = self.title_font.render("How To Play", True, MENU_TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 40)))
        lines = [
            "Move: Arrow keys or WASD",
            "Jump: Space",
            "Shoot: Z",
            "Melee: X",
            "Block: Shift | Parry: C",
            "Special: V",
            "Back",
        ]
        for i, line in enumerate(lines):
            color = MENU_TEXT_COLOR if i == self.menu_index else (50, 50, 50)
            text = self.menu_font.render(line, True, color)
            self.screen.blit(text, text.get_rect(center=(self.width // 2, 120 + i * 30)))
        self._draw_border()

    def _draw_credits(self) -> None:
        """Display a simple credits screen."""
        self.screen.fill(MENU_BG_COLOR)
        title = self.title_font.render("Credits", True, MENU_TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 40)))
        credits = [
            "Prototype by Hololive Fans",
            "Powered by Pygame",
            "Back",
        ]
        for i, line in enumerate(credits):
            color = MENU_TEXT_COLOR if i == self.menu_index else (50, 50, 50)
            text = self.menu_font.render(line, True, color)
            self.screen.blit(text, text.get_rect(center=(self.width // 2, 120 + i * 30)))
        self._draw_border()

    def _draw_scoreboard_menu(self) -> None:
        """Show best time and high score."""
        self.screen.fill(MENU_BG_COLOR)
        title = self.title_font.render("Records", True, MENU_TEXT_COLOR)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 40)))
        lines = [
            f"Best Time: {self.best_time}s",
            f"High Score: {self.best_score}",
            "Back",
        ]
        for i, line in enumerate(lines):
            color = MENU_TEXT_COLOR if i == self.menu_index else (50, 50, 50)
            text = self.menu_font.render(line, True, color)
            self.screen.blit(text, text.get_rect(center=(self.width // 2, 120 + i * 30)))
        self._draw_border()
