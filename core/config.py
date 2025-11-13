from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:admin@localhost:5432/Anand_crm"
    PROJECT_NAME: str = "Client Problem Resolution System"
    UPLOAD_DIR: str = "app/uploads"
    MAX_AUDIO_MB: int = 50

    # 🔥 REQUIRED JWT SETTINGS (these were missing!)
    SECRET_KEY: str = "supersecretkeychangeit"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
