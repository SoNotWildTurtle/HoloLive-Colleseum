class GuildManager:
    """Manage guild membership and ranks."""
    def __init__(self):
        self.members = {}

    def add_member(self, user: str, rank: str = "member") -> None:
        self.members[user] = rank

    def remove_member(self, user: str) -> None:
        self.members.pop(user, None)

    def set_rank(self, user: str, rank: str) -> None:
        if user in self.members:
            self.members[user] = rank

    def get_rank(self, user: str):
        return self.members.get(user)

    def list_members(self):
        return dict(self.members)
