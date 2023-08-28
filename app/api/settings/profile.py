from fastapi import APIRouter, Request, HTTPException
from ...db.config import SessionLocal
from ...db.schemas.User import User
from ...shared.helpers.jwt import check_access

router = APIRouter()
SECRET_KEY = 'my-secret-key'

# Considering the project requirements, I cannot use Pydantic for input validation and data serialization.
# IMPORTANT: I am treating the username as a full user dictionary since the user settings should be a separated settings group in a real application.
@router.put("/settings/profile")
def update_user_profile_settings(user: dict, request: Request):
    try:
        refresh_token_with_bearer = request.headers["Authorization"]
        refresh_token = refresh_token_with_bearer.split(" ")[1]

        refresh_token_payload = check_access(refresh_token, SECRET_KEY)

        if refresh_token_payload:
            user_id = refresh_token_payload["user_id"]

            session = SessionLocal()
            storedUser = session.query(User).filter(User.id == user_id).first()
            if not storedUser:
                raise HTTPException(status_code=400, detail="User does not exist")

            # Check that the username is not taken
            if user.get("username"):
                if session.query(User).filter(User.username == user["username"]).first():
                    raise HTTPException(status_code=400, detail="Username already exists")
            
            # Update the username
            if user.get("username"):
                storedUser.username = user["username"]

            session.commit()
            session.close()

            return {
                "message": "User profile updated successfully",
                "data": {
                    # "email": storedUser.email, # Error ?
                    "username": user["username"]
                }
            }

    except HTTPException as e:
        return {
            "error": {
                "message": e.detail,
                "status_code": e.status_code
            }
        }
