import hashlib
import secrets

def createSalt(nbBytes: int = 16) -> str:
    return secrets.token_hex(nbBytes)

def hash(text: str, salt: str = None) -> str:
    if salt is None:
        salt = createSalt(16)

    salted_password = text + salt

    hashed_password = hashlib.sha256(salted_password.encode("utf-8")).hexdigest()
    return f"{salt}${hashed_password}"

def validate_hash(text: str, stored_hashed_password: str) -> bool:
    stored_salt, hashed_password = stored_hashed_password.split('$')
    hashed_input_password = hash(text, stored_salt)
    print(hashed_input_password, stored_hashed_password)
    return hashed_input_password == stored_hashed_password
