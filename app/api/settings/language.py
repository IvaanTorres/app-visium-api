
from fastapi import APIRouter, Request, HTTPException
from ...db.config import SessionLocal
from ...db.schemas.User import User
from ...db.schemas.Preference import Preference
from ...shared.helpers.jwt import check_access

router = APIRouter()

SECRET_KEY = 'my-secret-key'

@router.put("/settings/language")
def update_language_settings(locale: dict, request: Request):
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

            # Update the locale
            if locale.get("locale"):
                storedPreference = session.query(Preference).filter(Preference.user_id == user_id).first()
                storedPreference.locale = locale["locale"]

            session.commit()
            session.close()

            return {
                "message": "User language settings updated successfully",
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


@router.get("/settings/language")
def get_language_settings(request: Request):
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
                "message": "User language settings retrieved successfully",
                "data": {
                    "locale": storedPreference.locale
                }
            }

    except HTTPException as e:
        return {
            "error": {
                "message": e.detail,
                "status_code": e.status_code
            }
        }
