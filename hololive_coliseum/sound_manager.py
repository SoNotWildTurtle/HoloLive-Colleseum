import os
import pygame


class SoundManager:
    """Manage mixer volume and track the last played sound."""

    def __init__(self, volume: float = 1.0):
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        self.volume = volume
        self.last_played = None
        self.mixer_ready = False
        try:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(self.volume)
            self.mixer_ready = True
        except pygame.error:
            self.mixer_ready = False

    def play(self, name: str) -> None:
        self.last_played = name

    def stop(self) -> None:
        self.last_played = None

    def cycle_volume(self) -> float:
        """Cycle master volume between 0%, 50% and 100%."""
        steps = [0.0, 0.5, 1.0]
        current = min(steps, key=lambda v: abs(v - self.volume))
        idx = steps.index(current)
        self.volume = steps[(idx + 1) % len(steps)]
        if self.mixer_ready:
            pygame.mixer.music.set_volume(self.volume)
        return self.volume

    def adjust_volume(self, delta: float) -> float:
        """Increment volume by *delta* within 0..1."""
        self.volume = max(0.0, min(1.0, self.volume + delta))
        if self.mixer_ready:
            pygame.mixer.music.set_volume(self.volume)
        return self.volume
