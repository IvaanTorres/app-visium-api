from pydantic import BaseModel
from typing import Optional

class RegistrationData(BaseModel):
    username: str
    password: str
    email: str
