
import secrets

def generate_secret_key():
    # Random URL-safe string of 32 bytes
    return secrets.token_urlsafe(32)