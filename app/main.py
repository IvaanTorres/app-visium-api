from fastapi import FastAPI
import uvicorn
from .db.config import engine, Base
from fastapi.middleware.cors import CORSMiddleware

from .api.user import router as user_router
from .api.settings.profile import router as settings_profile_router
from .api.settings.general import router as settings_general_router
from .api.settings.language import router as settings_language_router
from .api.login_infos import router as login_infos_router

# A good improvement would be to store the secret key in a secure secrets management system as HashiCorp Vault, AWS Secrets Manager, or a secure database
# Since I am not able to access for the specific user secret key from those services, I'll use the same for everyone.
# However, it's not a good practice to do so.
# It'd be better to fetch the user's secret key from the secrets management system and use it to generate the tokens.
# SECRET_KEY = generate_secret_key() # IMPORTANT: Everytime you restart the server, the change of secret will make the active tokens unusable
# SECRET_KEY = 'my-secret-key' will be same for everyone even if you restart the server

# Create the FastAPI instance
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Run migrations
Base.metadata.create_all(bind=engine)

# Routes
app.include_router(user_router)
app.include_router(settings_profile_router)
app.include_router(settings_general_router)
app.include_router(settings_language_router)
app.include_router(login_infos_router)

# Server running 
if __name__ == "__main__ ":
    uvicorn.run(app, host="0.0.0.0", port=8000)