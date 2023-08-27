from fastapi import FastAPI, HTTPException
import uvicorn
from .shared.helpers.jwt import create_jwt, validate_jwt
from .shared.helpers.hash import hash, validate_hash, createSalt
from .shared.helpers.secrets import generate_secret_key
from .shared.constants.jwt import header
from .shared.helpers.date import calculate_future_time
from .models.User import UserModel
from .db.schemas.User import User
from .db.schemas.Token import Token
from .db.schemas.Login import Login
from .db.schemas.Preference import Preference
from .db.config import SessionLocal, engine, Base

# Create the FastAPI instance
app = FastAPI()

# Run migrations
Base.metadata.create_all(bind=engine)

# Considering the project requirements, I cannot use Pydantic for input validation and data serialization.
@app.post("/register")
def register(data: dict):
    session = SessionLocal()

    userModel = UserModel(**data)

    # Validate the data
    try:
        if not userModel.username:
            raise HTTPException(status_code=400, detail="Username is required")
        if not userModel.password:
            raise HTTPException(status_code=400, detail="Password is required")
        if not userModel.email:
            raise HTTPException(status_code=400, detail="Email is required")
        if session.query(User).filter(User.username == userModel.username).first():
            raise HTTPException(status_code=400, detail="Username already exists")
        if session.query(User).filter(User.email == userModel.email).first():
            raise HTTPException(status_code=400, detail="Email already exists")
        if any(char in userModel.username for char in "<>&%${}'\"\\/()"):
            raise HTTPException(status_code=400, detail="Username contains invalid characters")
        if any(char in userModel.password for char in "<>&%${}'\"\\/()"):
            raise HTTPException(status_code=400, detail="Password contains invalid characters")
        if any(char in userModel.email for char in "<>&%${}'\"\\/()"):
            raise HTTPException(status_code=400, detail="Email contains invalid characters")
        
    except Exception as e:
        return {"error": e}
    
    # Hash the password
    salt = createSalt(16)
    hashed_password = hash(userModel.password, salt)

    # Generate the secret key for both tokens
    # A good improvement would be to store the secret key in a secure secrets management system as HashiCorp Vault, AWS Secrets Manager, or a secure database
    user_secret = generate_secret_key()
    # Generate the access token
    access_expiration_time = 15 # 15 minutes
    access_token = create_jwt(
        header, 
        {
            "sub": userModel.username, 
            "exp": calculate_future_time(access_expiration_time)
        }, 
        user_secret
    )

    # Generate the refresh token
    refresh_expiration_time = 60 * 24 * 7 # 1 week
    refresh_token = create_jwt(
        header, 
        {
            "sub": userModel.username, 
            "exp": calculate_future_time(refresh_expiration_time)
        }, 
        user_secret
    )

    # Set and store the user data, their token, their preferences, and their login count
    user = User(username=userModel.username, password=hashed_password, email=userModel.email)
    token = Token(token=refresh_token, user=user)
    login = Login(nb_logins=1, user=user)
    # TODO: Get the user's locale from the request (manage the UI select state)
    preference = Preference(locale="en_EN", user=user)

    session.add(user)
    session.add(token)
    session.add(login)
    session.add(preference)
    session.commit()
    session.close()

    return {
        "message": "User registered successfully",
        "access_token": access_token,
        "refresh_token": refresh_token
    }

# Server running 
if __name__ == "__main__ ":
    uvicorn.run(app, host="0.0.0.0", port=8000)