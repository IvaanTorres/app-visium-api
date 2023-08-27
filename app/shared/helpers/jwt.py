import hmac
import base64
import json
import hashlib
from datetime import datetime
from typing import Dict

def encode_base64(data: bytes) -> str:
    base64_bytes = base64.urlsafe_b64encode(data)
    return base64_bytes.decode('ascii').rstrip("=")

def generate_jwt_signature(secret_key, data):
    signature = hmac.new(secret_key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256)
    return base64.urlsafe_b64encode(signature.digest()).decode('utf-8')

def create_jwt(header: Dict, payload: Dict, secret: str) -> str:
    encoded_header = encode_base64(json.dumps(header).encode('utf-8'))
    encoded_payload = encode_base64(json.dumps(payload).encode('utf-8'))

    signature_input = f"{encoded_header}.{encoded_payload}"
    signature = generate_jwt_signature(secret, signature_input)
    encoded_signature = encode_base64(signature.encode('utf-8'))

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
        encoded_signature_input = f"{header_base64}.{payload_base64}"
        expected_signature = generate_jwt_signature(secret, encoded_signature_input)
        actual_signature = base64.urlsafe_b64decode(signature + "==")


        if not hmac.compare_digest(expected_signature.encode('utf-8'), actual_signature):
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