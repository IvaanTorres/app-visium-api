from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from ..db.config import SessionLocal
from ..models.User import UserModel
from ..db.schemas.User import User
from ..db.schemas.Token import Token
from ..db.schemas.Login import Login
from ..db.schemas.Preference import Preference
import re
from ..shared.helpers.hash import hash, validate_hash, createSalt
from ..shared.helpers.jwt import create_jwt
from ..shared.helpers.date import calculate_future_time
from ..shared.helpers.jwt import check_access
from ..shared.constants.jwt import header

router = APIRouter()

SECRET_KEY = 'my-secret-key'

# ------------------------------- LOGIN SYSTEM ------------------------------- #

# Considering the project requirements, I cannot use Pydantic for input validation and data serialization.
@router.post("/register")
def register(data: dict):
    session = SessionLocal()

    userModel = UserModel(username=data["username"], password=data["password"], email=data["email"])

    # Validate the data
    password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})"
    user_pattern = r"^[a-zA-Z0-9_.]{3,20}$"
    email_pattern = r"\S+@\S+\.\S+"

    try:
        if not userModel.username:
            raise HTTPException(status_code=400, message="Username is required")
        if not userModel.password:
            raise HTTPException(status_code=400, message="Password is required")
        if not userModel.email:
            raise HTTPException(status_code=400, message="Email is required")
        if session.query(User).filter(User.username == userModel.username).first():
            raise HTTPException(status_code=400, message="Username already exists")
        if session.query(User).filter(User.email == userModel.email).first():
            raise HTTPException(status_code=400, message="Email already exists")
        if not re.match(user_pattern, userModel.username):
            raise HTTPException(status_code=400, message="Username contains invalid characters")
        if not re.match(password_pattern, userModel.password):
            raise HTTPException(status_code=400, message="Password contains invalid characters")
        if not re.match(email_pattern, userModel.email):
            raise HTTPException(status_code=400, message="Email contains invalid characters")
        
    except Exception as e:
        return {"error": e}
    
    # Hash the password
    salt = createSalt(16)
    hashed_password = hash(userModel.password, salt)

    # Set and store the user data, their token, their preferences, and their login count
    user = User(username=userModel.username, password=hashed_password, email=userModel.email)
    session.add(user)
    session.commit()

    stored_user = session.query(User).filter(User.username == userModel.username).first()
    # Generate the secret key for both tokens
    # A good improvement would be to store the secret key in a secure secrets management system as HashiCorp Vault, AWS Secrets Manager, or a secure database
    # user_secret = generate_secret_key()
    # Generate the access token
    access_expiration_time = 1
    access_token = create_jwt(
        header, 
        {
            "user_id": stored_user.id, 
            "exp": calculate_future_time(access_expiration_time)
        }, 
        SECRET_KEY
    )

    # Generate the refresh token
    refresh_expiration_time = 24
    refresh_token = create_jwt(
        header, 
        {
            "user_id": stored_user.id, 
            "exp": calculate_future_time(refresh_expiration_time)
        }, 
        SECRET_KEY
    )

    token = Token(token=refresh_token, user=user)
    login = Login(nb_logins=1, user=user)
    preference = Preference(locale=data["locale"], user=user)

    session.add(token)
    session.add(login)
    session.add(preference)
    session.commit()
    session.close()

    return {
        "message": "User registered successfully",
        "data": {
            "access_token": {
                "token": access_token,
                "expires_in": calculate_future_time(access_expiration_time)
            },
            "refresh_token": {
                "token": refresh_token,
                "expires_in": calculate_future_time(refresh_expiration_time)
            }
        }
    }

# Considering the project requirements, I cannot use Pydantic for input validation and data serialization.
@router.post("/login")
def login(data: dict):
    session = SessionLocal()

    if data.get("username"):
        user = UserModel(username=data["username"], password=data["password"])
    elif data.get("email"):
        user = UserModel(email=data["email"], password=data["password"])



    # Validate the data
    password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})"
    user_pattern = r"^[a-zA-Z0-9_.]{3,20}$"
    email_pattern = r"\S+@\S+\.\S+"

    print(user.username, user.password, user.email)
    try:
        if not user.username and not user.email:
            raise HTTPException(status_code=400, message="Username or email is required")
        if not user.password:
            raise HTTPException(status_code=400, message="Password is required")
        if user.username and not re.match(user_pattern, user.username):
            raise HTTPException(status_code=400, message="Username contains invalid characters")
        if not re.match(password_pattern, user.password):
            raise HTTPException(status_code=400, message="Password contains invalid characters")
        if user.email and not re.match(email_pattern, user.email):
            raise HTTPException(status_code=400, message="Email contains invalid characters")
        
        # Check if the user or email exists
        if user.username:
            if not session.query(User).filter(User.username == user.username).first():
                raise HTTPException(status_code=400, message="Username does not exist")
        if user.email:
            if not session.query(User).filter(User.email == user.email).first():
                raise HTTPException(status_code=400, message="Email does not exist")
        
    except Exception as e:
        return {"error": e}
    
    storedUser = None
    if user.username:
        storedUser = session.query(User).filter(User.username == user.username).first()
    if user.email:
        storedUser = session.query(User).filter(User.email == user.email).first()
    
    # Verify the password
    try: 
        is_valid = validate_hash(user.password, storedUser.password)
        if not is_valid:
            raise HTTPException(status_code=400, message="Password is invalid")
    except Exception as e:
        return {"error": e}

    # Generate the secret key for both tokens
    # A good improvement would be to store the secret key in a secure secrets management system as HashiCorp Vault, AWS Secrets Manager, or a secure database
    # user_secret = generate_secret_key()
    # Generate the access token
    access_expiration_time = 1 # 1h
    access_token = create_jwt(
        header, 
        {
            "user_id": storedUser.id, 
            "exp": calculate_future_time(access_expiration_time),
        }, 
        SECRET_KEY
    )

    # Generate the refresh token
    refresh_expiration_time = 24 # hours
    refresh_token = create_jwt(
        header, 
        {
            "user_id": storedUser.id, 
            "exp": calculate_future_time(refresh_expiration_time)
        }, 
        SECRET_KEY
    )

    # +1 to the loggin count and add the refresh token
    login = session.query(Login).filter(Login.user_id == storedUser.id).first()
    login.nb_logins += 1

    token = Token(token=refresh_token, user=storedUser)
    
    preference = session.query(Preference).filter(Preference.user_id == storedUser.id).first()
    preference.locale = data["locale"]

    session.add(login)
    session.add(token)
    session.commit()
    session.close()

    return {
        "message": "User logged in successfully",
        "data": {
            "access_token": {
                "token": access_token,
                "expires_in": calculate_future_time(access_expiration_time)
            },
            "refresh_token": {
                "token": refresh_token,
                "expires_in": calculate_future_time(refresh_expiration_time)
            }
        }
    }

# Considering the project requirements, I cannot use Pydantic for input validation and data serialization.
@router.post("/logout")
def logout(request: Request):
    # refresh_token = request.cookies.get("x-refresh-token")
    refresh_token_with_bearer = request.headers["Authorization"]
    refresh_token = refresh_token_with_bearer.split(" ")[1]

    try:
        if not refresh_token:
            raise HTTPException(status_code=400, message="Token is required")
    except Exception as e:
        return {"error": e}
    
    # Revoke the token
    try:
        session = SessionLocal()
        storedToken = session.query(Token).filter(Token.token == refresh_token).first()
        if not storedToken:
            raise HTTPException(status_code=400, message="Token does not exist")

        storedToken.is_revoked = 1

        session.commit()
        session.close()
    except Exception as e:
        return {"error": e}

    response = JSONResponse(content={
        "message": "Logged out successfully",
        "data": {
            "is_logged_out": True
        }
    })
    # response.delete_cookie(key="x-refresh-token")  # Clear the cookie
    return response


# ------------------------------- USER SYSTEM ------------------------------- #
# Considering the project requirements, I cannot use Pydantic for input validation and data serialization.
@router.delete("/delete-account")
def delete_account(request: Request):
    try:
        refresh_token_with_bearer = request.headers["Authorization"]
        refresh_token = refresh_token_with_bearer.split(" ")[1]

        access_token_payload = check_access(refresh_token, SECRET_KEY)

        if access_token_payload:
            user_id = access_token_payload["user_id"]

            session = SessionLocal()
            storedUser = session.query(User).filter(User.id == user_id).first()
            if not storedUser:
                raise HTTPException(status_code=400, message="User does not exist")

            # Delete tokens (sessions) linked to user
            storedTokens = session.query(Token).filter(Token.user_id == user_id).all()
            for token in storedTokens:
                session.delete(token)

            # Delete the login records linked to user
            storedLogin = session.query(Login).filter(Login.user_id == user_id).first()
            session.delete(storedLogin)

            # Delete the preferences linked to user
            storedPreference = session.query(Preference).filter(Preference.user_id == user_id).first()
            session.delete(storedPreference)

            session.delete(storedUser)
            session.commit()
            session.close()


            return {
                "message": "User deleted successfully",
                "data": {
                    "is_deleted": True
                }
            }
    except Exception as e:
        return {"error": e}


@router.get("/user")
def get_user(request: Request):
    try:
        refresh_token_with_bearer = request.headers["Authorization"]
        refresh_token = refresh_token_with_bearer.split(" ")[1]

        refresh_token_payload = check_access(refresh_token, SECRET_KEY)

        if refresh_token_payload:
            user_id = refresh_token_payload["user_id"]

            session = SessionLocal()
            storedUser = session.query(User).filter(User.id == user_id).first()
            if not storedUser:
                raise HTTPException(status_code=400, message="User does not exist")

            session.close()

            return {
                "message": "User retrieved successfully",
                "data": {
                    "username": storedUser.username,
                    "email": storedUser.email
                }
            }

    except Exception as e:
        return {"error": e}
