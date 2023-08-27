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
        print("Expected signature", expected_signature)
        actual_signature = base64.urlsafe_b64decode(signature + "==")

        if not hmac.compare_digest(expected_signature.encode('utf-8'), actual_signature):
            print("Invalid signature")
            return False
        
        print("Valid signature", payload.get("exp"))

        # Check expiration
        current_time = datetime.utcnow()
        # Convert the first datetime string to a datetime object
        # datetime_obj_1 = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S.%f")

        # Convert the second datetime string to a datetime object
        # Remove the trailing 'Z' and parse the string
        datetime_obj = datetime.strptime(payload.get("exp")[:-1], "%Y-%m-%dT%H:%M:%S.%f")

        print("Current time", datetime_obj)


        # if payload.get("exp"):
        #     print("Checking expiration")
        #     expiration_time = datetime.fromtimestamp(current_time)
        #     if current_time > expiration_time:
        #         print("Token has expired")
        #         return False

        return True
    except:
        int("Invalid token")
        return False