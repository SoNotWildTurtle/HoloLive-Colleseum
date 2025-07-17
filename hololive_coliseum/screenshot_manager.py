class ScreenshotManager:
    """Manage in-game screenshots."""

    def __init__(self):
        self.shots = []

    def capture(self, image: str) -> None:
        self.shots.append(image)

    def list_shots(self):
        return list(self.shots)
