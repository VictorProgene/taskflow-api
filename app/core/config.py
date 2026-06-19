import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "TaskFlow API"
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Novas configurações para a Fase 3
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # O token expira em 1 hora


settings = Settings()