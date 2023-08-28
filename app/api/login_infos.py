
from fastapi import APIRouter, Request, HTTPException
from ..shared.helpers.jwt import check_access
from ..db.config import SessionLocal
from ..db.schemas.User import User
from ..db.schemas.Login import Login

router = APIRouter()

SECRET_KEY = 'my-secret-key'

@router.get("/info/login")
def get_info_login(request: Request):
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

            storedLogin = session.query(Login).filter(Login.user_id == user_id).first()

            session.close()

            return {
                "message": "User login info retrieved successfully",
                "data": {
                    "nb_logins": storedLogin.nb_logins
                }
            }

    except Exception as e:
        return {"error": e}
