import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")
class Settings:
    # In a real application, this should be loaded from an environment variable
    # For example: os.getenv("SECRET_KEY")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    print("Security key")
    print(SECRET_KEY)
    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")


settings = Settings()
