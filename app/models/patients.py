from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, index=True)
    age = Column(Integer)
    health_issues = Column(Text, nullable=True)

    medical_records = relationship("MedicalRecord", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")
