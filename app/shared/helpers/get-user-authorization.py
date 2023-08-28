from fastapi import HTTPException, Request
from .jwt import check_access
from ...db.config import SessionLocal, engine, Base
from ...db.schemas.User import User

def get_user_authorization(secret_key: str, request: Request):
  refresh_token_with_bearer = request.headers["Authorization"]
  refresh_token = refresh_token_with_bearer.split(" ")[1]

  access_token_payload = check_access(refresh_token, secret_key)

  if access_token_payload:
      user_id = access_token_payload["user_id"]

      # TODO: Check
      session = SessionLocal()
      storedUser = session.query(User).filter(User.id == user_id).first()
      if not storedUser:
          raise HTTPException(status_code=400, message="User does not exist")
      
      session.close()
      return storedUser