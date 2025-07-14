class AuthManager:
    """Handle account credentials and simple session tokens."""

    def __init__(self):
        self.users = {}
        self.tokens = {}

    def register(self, username: str, password: str) -> None:
        self.users[username] = password

    def login(self, username: str, password: str):
        if self.users.get(username) == password:
            token = f"{username}-token"
            self.tokens[token] = username
            return token
        return None

    def verify(self, token: str) -> bool:
        return token in self.tokens
