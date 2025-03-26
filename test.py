from app.db.database import Base
from sqlalchemy import create_engine
  # Ensure this contains your correct DB URL
from app.db.database import Base
from pydantic_settings import BaseSettings
DATABASE_URL= "postgresql://postgres:Manish@localhost:5432/shrms_db"

engine = create_engine(DATABASE_URL)

# Check detected tables
print(Base.metadata.tables.keys())
