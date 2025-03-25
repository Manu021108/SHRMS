from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.doctors import DoctorCreate, DoctorUpdate, DoctorResponse
from app.db.database import get_db
from app.api.routes.auth import get_current_active_user
from app.schemas.auth import User
from app.models.doctors import Doctor

router = APIRouter()

# CRUD operations
def get_doctor(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()

def get_doctors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Doctor).offset(skip).limit(limit).all()

def create_doctor(db: Session, doctor: DoctorCreate):
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def update_doctor(db: Session, doctor_id: int, doctor: DoctorUpdate):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if db_doctor:
        for key, value in doctor.dict().items():
            setattr(db_doctor, key, value)
        db.commit()
        db.refresh(db_doctor)
    return db_doctor

def delete_doctor(db: Session, doctor_id: int):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if db_doctor:
        db.delete(db_doctor)
        db.commit()
    return db_doctor

# API endpoints
@router.post("/", response_model=DoctorResponse)
async def create_doctor_endpoint(doctor: DoctorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_doctor(db, doctor)

@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor_endpoint(doctor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    doctor = get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.get("/", response_model=List[DoctorResponse])
async def get_doctors_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return get_doctors(db, skip=skip, limit=limit)

@router.put("/{doctor_id}", response_model=DoctorResponse)
async def update_doctor_endpoint(doctor_id: int, doctor: DoctorUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    updated_doctor = update_doctor(db, doctor_id, doctor)
    if not updated_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return updated_doctor

@router.delete("/{doctor_id}", response_model=DoctorResponse)
async def delete_doctor_endpoint(doctor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    deleted_doctor = delete_doctor(db, doctor_id)
    if not deleted_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return deleted_doctor