# from models.User import RegistrationData
from fastapi import FastAPI
import uvicorn
from sqlalchemy import create_engine, Column, String
import hmac
import base64
import json
import hashlib
from typing import Dict
import datetime
from pydantic import BaseModel
from typing import Optional

class RegistrationData(BaseModel):
    username: str
    password: str
    email: str
import secrets
# from db.config import SessionLocal, Base, engine

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://root:root@db:5432/visium"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


app = FastAPI()

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    password = Column(String(length=100))
    email = Column(String, index=True)

# Base.metadata.create_all(bind=engine)

# ---------------------------------- SECRETS --------------------------------- #
def generate_secret_key():
    # Random URL-safe string of 32 bytes
    return secrets.token_urlsafe(32)

# ------------------------------------ JWT ----------------------------------- #
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

# --------------------------------- PASSWORD --------------------------------- #
def hash_password(password: str, salt: str = None) -> str:
    if salt is None:
        salt = secrets.token_hex(16)  # Generate a random salt

    salted_password = password + salt

    hashed_password = hashlib.sha256(salted_password.encode("utf-8")).hexdigest()
    return f"{salt}${hashed_password}"

def validate_password(password: str, stored_hashed_password: str) -> bool:
    stored_salt, hashed_password = stored_hashed_password.split('$')
    hashed_input_password = hash_password(password, stored_salt)
    return hashed_input_password == stored_hashed_password


@app.get("/")
def generate_jwt(duration: int = 1):

    # TODO: JWT (HMAC-SHA256 MAC)
    current_time = datetime.datetime.utcnow()
    expiration_time = current_time + datetime.timedelta(hours=duration)

    header = {
        "alg": "HS256", 
        "typ": "JWT"     
    }
    payload = {
        "sub": "user123",
        "exp": int(expiration_time.timestamp())
    }

    # IMPORTANT: Store the random secret into secure secrets management system as HashiCorp Vault, AWS Secrets Manager, or a secure database
    secret = generate_secret_key()
    jwt = create_jwt(header, payload, secret)
    validated_jwt = validate_jwt(jwt, secret)

    return {
        "jwt": jwt,
        "validated_jwt": validated_jwt
    }

    # TODO: PASSWORD (HASHING)
    # password = "123456"
    # hashed_password = hash_password(password)
    # validated_password = validate_password(password, hashed_password)
    # print(validated_password)

@app.post("/register")
def register(user: RegistrationData):
    session = SessionLocal()
    # Check if the user already exists (username or email)
    if session.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    if session.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Generate a random salt and hash the password
    salt = secrets.token_hex(16)
    hashed_password = hash_password(user.password, salt)

    # Store the user data (replace this with actual database storage)
    user = User(username=user.username, password=hashed_password, email=user.email)
    session.add(user)
    session.commit()
    session.close()

    return {"message": "User registered successfully"}

# Server running 
if __name__ == "__main__ ":
    uvicorn.run(app, host="0.0.0.0", port=8000)