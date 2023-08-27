class UserModel:
    def __init__(self, password: str, username: str = None,  email: str = None):
        self.username = username
        self.password = password
        self.email = email
