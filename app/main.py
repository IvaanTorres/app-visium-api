from fastapi import FastAPI
import uvicorn
# from db.config import engine
import hmac
import base64
import json
import hashlib
from typing import Dict
import datetime


import secrets

app = FastAPI()

# ---------------------------------- SECRETS --------------------------------- #
def encrypt(encryption_key, plaintext):
    encrypted = []
    for i in range(len(plaintext)):
        key_char = encryption_key[i % len(encryption_key)]
        encrypted_char = chr(ord(plaintext[i]) ^ ord(key_char))
        encrypted.append(encrypted_char)
    return ''.join(encrypted)

def decrypt(decryption_key, ciphertext):
    decrypted = []
    for i in range(len(ciphertext)):
        key_char = decryption_key[i % len(decryption_key)]
        decrypted_char = chr(ord(ciphertext[i]) ^ ord(key_char))
        decrypted.append(decrypted_char)
    return ''.join(decrypted)

# ------------------------------------ JWT ----------------------------------- #
def encode_base64(data: bytes) -> str:
    base64_bytes = base64.urlsafe_b64encode(data)
    return base64_bytes.decode('ascii').rstrip("=")

def create_jwt(header: Dict, payload: Dict) -> str:
    encoded_header = encode_base64(json.dumps(header).encode('utf-8'))
    encoded_payload = encode_base64(json.dumps(payload).encode('utf-8'))

    signature_input = f"{encoded_header}.{encoded_payload}".encode('ascii')
    signature = hmac.new(generate_jwt(), signature_input, hashlib.sha256)
    encoded_signature = encode_base64(signature.digest())

    jwt = f"{encoded_header}.{encoded_payload}.{encoded_signature}"
    return jwt

def validate_jwt(token, secret):
    try:
        # Split the token into its header and payload
        header_base64, payload_base64, signature = token.split(".")

        # Decode the header and payload
        header = json.loads(base64.urlsafe_b64decode(header_base64 + "==").decode("utf-8"))
        payload = json.loads(base64.urlsafe_b64decode(payload_base64 + "==").decode("utf-8"))

        # Verify the signature
        encoded_signature_input = f"{header_base64}.{payload_base64}".encode("utf-8")
        expected_signature = hmac.new(secret, encoded_signature_input, hashlib.sha256).digest()
        actual_signature = base64.urlsafe_b64decode(signature + "==")


        if not hmac.compare_digest(expected_signature, actual_signature):
            print("Invalid signature")
            return False
        
        print("Valid signature")


        # Check expiration
        current_time = datetime.datetime.utcnow()
        if payload.get("exp") and current_time > datetime.datetime.fromtimestamp(payload["exp"]):
            print("Token has expired")
            return False

        return True
    except:
        print("Invalid token")
        return False

# --------------------------------- PASSWORD --------------------------------- #
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def validate_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password


@app.get("/")
def generate_jwt():

    # TODO: JWT (HMAC-SHA256 MAC)
    # Example header and payload (you can customize these)
    # header = {
    #     "alg": "HS256",  # Algorithm used for signature
    #     "typ": "JWT"     # Type of token
    # }
    # payload = {
    #     "sub": "user123",  # Subject
    #     "exp": 1672531200  # Expiration time (example: 01/01/2023)
    # }

    # jwt = create_jwt(header, payload)
    # validated_jwt = validate_jwt(jwt, SECRET_KEY)

    # return {
    #     "jwt": jwt,
    #     "validated_jwt": validated_jwt
    # }

    # TODO: SECRETS (ENCRYPTION)
    # Example usage
    password = "1234"
    jwt_secret = "Secret"

    encrypted_data = encrypt(password, jwt_secret)
    print("Encrypted:", encrypted_data)

    decrypted_data = decrypt(password, encrypted_data)
    print("Decrypted:", decrypted_data)

    # TODO: PASSWORD (HASHING)
    # password = "123456"
    # hashed_password = hash_password(password)
    # validated_password = validate_password(password, hashed_password)
    # print(validated_password)

# Server running 
if __name__ == "__main__ ":
    uvicorn.run(app, host="0.0.0.0", port=8000)