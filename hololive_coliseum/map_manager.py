class MapManager:
    """Store available maps and the currently active one."""
    def __init__(self):
        self.maps = {}
        self.current = None

    def add_map(self, name: str, data) -> None:
        self.maps[name] = data

    def set_current(self, name: str) -> bool:
        if name in self.maps:
            self.current = name
            return True
        return False

    def get_current(self):
        return self.maps.get(self.current)
