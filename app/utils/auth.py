from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy_password")


def generate_hash_password(password: str) -> str:
    return password_hash.hash(password=password)

def verify_hash_password(login_password: str, stored_hash_password: str):
    return password_hash.verify(password=login_password, hash=stored_hash_password)

