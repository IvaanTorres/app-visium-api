from fastapi import FastAPI
import uvicorn
import datetime
from .shared.helpers.jwt import create_jwt, validate_jwt
from .shared.helpers.hash import hash, validate_hash, createSalt
from .shared.helpers.secrets import generate_secret_key
from .models.User import RegistrationData
from .db.schemas.schemas import User
from .db.config import SessionLocal, engine, Base

# Create the FastAPI instance
app = FastAPI()

# Run migrations
Base.metadata.create_all(bind=engine)

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

    if session.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    if session.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password
    salt = createSalt(16)
    hashed_password = hash(user.password, salt)

    # Store the user data (replace this with actual database storage)
    user = User(username=user.username, password=hashed_password, email=user.email)
    session.add(user)
    session.commit()
    session.close()

    return {"message": "User registered successfully"}

# Server running 
if __name__ == "__main__ ":
    uvicorn.run(app, host="0.0.0.0", port=8000)