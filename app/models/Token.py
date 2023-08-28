# Pydantic is not allowed in the user requirements for data validation, etc
class TokenModel:
    def __init__(self, token: str, is_revoked: bool = False):
        self.token = token
        self.is_revoked = is_revoked
