class EquipmentManager:
    """Manage equipment slots for a player."""

    def __init__(self) -> None:
        self.slots = {
            "weapon": None,
            "armor": None,
            "accessory": None,
        }

    def equip(self, slot: str, item) -> None:
        """Equip an item in the given slot."""
        if slot in self.slots:
            self.slots[slot] = item

    def unequip(self, slot: str) -> None:
        """Remove whatever is equipped in the slot."""
        if slot in self.slots:
            self.slots[slot] = None

    def get(self, slot: str):
        """Return the item equipped in the slot or ``None``."""
        return self.slots.get(slot)
