from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:Kranti%4021@localhost:5432/cprs_db"
    PROJECT_NAME: str = "Client Problem Resolution System"
    UPLOAD_DIR: str = "app/uploads"
    MAX_AUDIO_MB: int = 50

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
