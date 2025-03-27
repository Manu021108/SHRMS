from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"))
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"))
    medicine_id = Column(Integer, ForeignKey("medicines.id", ondelete="CASCADE"))
    dosage = Column(String, nullable=False)
    instructions = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")
    medicine = relationship("Medicine", back_populates="prescriptions")