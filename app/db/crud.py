# app/db/crud.py
from app.schemas.doctors import DoctorCreate, DoctorResponse
from app.db import SessionLocal, engine
from app.db import Doctor

def create_doctor(doctor: DoctorCreate) -> DoctorResponse:
    db = SessionLocal()
    db_doctor = Doctor(name=doctor.name, email=doctor.email, specialty=doctor.specialty)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return DoctorResponse.from_orm(db_doctor)