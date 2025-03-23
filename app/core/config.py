from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Explicitly load environment variables
load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    MONGODB_URI: str = os.getenv("MONGODB_URI")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")

    class Config:
        from_attributes = True  # Fix for Pydantic V2

settings = Settings()

print(f"SECRET_KEY: {settings.SECRET_KEY}")  # Debugging
print(f"MONGODB_URI: {settings.MONGODB_URI}")  # Debugging
print(f"DATABASE_NAME: {settings.DATABASE_NAME}")  # Debugging
