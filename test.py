from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv(override=True)

client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("DATABASE_NAME")]

user = db.users.find_one({"email": "manish@example.com"})
print("User in DB:", user)
