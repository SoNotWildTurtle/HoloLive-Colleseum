class AccessibilityManager:
    """Store toggles for accessibility features."""

    def __init__(self):
        self.options = {"colorblind": False, "font_scale": 1.0}

    def toggle(self, name: str) -> None:
        if name in self.options and isinstance(self.options[name], bool):
            self.options[name] = not self.options[name]
