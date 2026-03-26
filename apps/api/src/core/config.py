import os
from dotenv import load_dotenv
from pathlib import Path

# Correctly load the .env file from the `apps/api` directory
dotenv_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)


class Settings:
    # In a real application, this should be loaded from an environment variable
    # For example: os.getenv("SECRET_KEY")
    SECRET_KEY: str = os.getenv("SECURITY_KEY", "a_default_secret_key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")


settings = Settings()
