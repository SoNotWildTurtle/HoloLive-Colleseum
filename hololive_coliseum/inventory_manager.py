class InventoryManager:
    """Track items collected during play."""

    def __init__(self) -> None:
        self.items: dict[str, int] = {}

    def add(self, item: str, count: int = 1) -> None:
        self.items[item] = self.items.get(item, 0) + count

    def remove(self, item: str, count: int = 1) -> bool:
        current = self.items.get(item, 0)
        if current < count:
            return False
        new = current - count
        if new:
            self.items[item] = new
        else:
            self.items.pop(item, None)
        return True

    def has(self, item: str) -> bool:
        return item in self.items

    def count(self, item: str) -> int:
        return self.items.get(item, 0)

    def to_dict(self) -> dict[str, int]:
        return dict(self.items)

    def load_from_dict(self, data: dict[str, int]) -> None:
        self.items = dict(data)

