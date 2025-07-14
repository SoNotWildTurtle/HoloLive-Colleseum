class DataProtectionManager:
    """Provide simple XOR encryption for data in transit."""

    def __init__(self, key: bytes = b""):
        self.key = key

    def encrypt(self, data: bytes) -> bytes:
        if not self.key:
            return data
        return bytes(b ^ self.key[i % len(self.key)] for i, b in enumerate(data))

    def decrypt(self, data: bytes) -> bytes:
        return self.encrypt(data)
