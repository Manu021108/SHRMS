from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    details = Column(String, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"))

    # ✅ Link only to patients
    patient = relationship("Patient", back_populates="prescriptions")
