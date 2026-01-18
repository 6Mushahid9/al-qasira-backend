from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    APP_NAME: str = ""
    FRONTEND_ORIGIN: str = ""

    ADMIN_PASSWORD_HASH: str = ""
    SESSION_SECRET_KEY: str = ""

    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_CLIENT_EMAIL: str = ""
    FIREBASE_PRIVATE_KEY: str = ""

    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
