from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://projectAG_user:projectAG_1988@localhost:7777/Anand_crm"
    PROJECT_NAME: str = "Client Problem Resolution System"
    UPLOAD_DIR: str = "app/uploads"
    MAX_AUDIO_MB: int = 50

    # 🔥 JWT Settings
    SECRET_KEY: str = "supersecretkeychangeit"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # 📧 Email Settings
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_pass: str
    email_from: str
    email_to: str
    email_subject: str
    email_template: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()