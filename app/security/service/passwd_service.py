from pwdlib import PasswordHash


class PasswordService:
    def __init__(self):
        self._password_hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self._password_hash.hash(password=password)

    def verify(self, password: str, hashed: str) -> bool:
        return self._password_hash.verify(password=password, hash=hashed)

    def needs_rehash(self, password: str, password_hash: str) -> str:
        return self._password_hash.verify_and_update(password=password, password_hash=password_hash)