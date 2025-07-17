class EnvironmentManager:
    """Track environment settings like weather or time of day."""
    def __init__(self):
        self.settings = {}

    def set(self, key: str, value) -> None:
        self.settings[key] = value

    def get(self, key: str, default=None):
        return self.settings.get(key, default)
