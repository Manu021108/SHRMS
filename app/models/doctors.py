from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base  # ✅ Import Base from models/__init__.py

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    appointments = relationship("Appointment", back_populates="doctor")
