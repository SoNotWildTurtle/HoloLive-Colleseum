class SoundManager:
    """Track the last played sound effect."""

    def __init__(self):
        self.last_played = None

    def play(self, name: str) -> None:
        self.last_played = name

    def stop(self) -> None:
        self.last_played = None
