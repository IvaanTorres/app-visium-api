from fastapi import APIRouter, Request, HTTPException
from ...db.config import SessionLocal
from ...db.schemas.User import User
from ...db.schemas.Preference import Preference
from ...shared.helpers.jwt import check_access

router = APIRouter()
SECRET_KEY = 'my-secret-key'

@router.put("/settings/general")
def update_user_profile_settings(general_preferences: dict, request: Request):
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

            if general_preferences.get("welcomingMessageSize"):
                if not isinstance(general_preferences["welcomingMessageSize"], int):
                    raise HTTPException(status_code=400, detail="Welcoming message size must be an integer")

            # Update the welcoming message size
            if general_preferences.get("welcomingMessageSize"):
                storedPreference = session.query(Preference).filter(Preference.user_id == user_id).first()
                storedPreference.welcomingMessageSize = general_preferences["welcomingMessageSize"]

            session.commit()
            session.close()

            return {
                "message": "User general preferences updated successfully",
                "data": {
                    "is_updated": True
                }
            }

    except HTTPException as e:
        return {
            "error": {
                "message": e.detail,
                "status_code": e.status_code
            }
        }

@router.get("/settings/general")
def get_general_settings(request: Request):
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

            storedPreference = session.query(Preference).filter(Preference.user_id == user_id).first()

            session.close()

            return {
                "message": "User general settings retrieved successfully",
                "data": {
                    "welcomingMessageSize": storedPreference.welcomingMessageSize,
                }
            }

    except HTTPException as e:
        return {
            "error": {
                "message": e.detail,
                "status_code": e.status_code
            }
        }
