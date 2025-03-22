import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings:
    MONGODB_URI: str = os.getenv("mongodb+srv://manishpandey021108:U9UJtLSz8XcCE2pG@shrsh.gxpa4.mongodb.net/")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "SHRSH")

settings = Settings()