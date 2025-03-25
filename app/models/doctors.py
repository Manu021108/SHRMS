from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialty = Column(String)
    email = Column(String, unique=True, index=True)