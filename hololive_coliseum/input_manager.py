class InputManager:
    """Handle key and controller mappings."""

    def __init__(self, mappings=None):
        self.mappings = dict(mappings or {})

    def get(self, action: str):
        return self.mappings.get(action)

    def set(self, action: str, key) -> None:
        self.mappings[action] = key
