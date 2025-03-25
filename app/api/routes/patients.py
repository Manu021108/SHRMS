from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.patients import PatientCreate, PatientUpdate, PatientResponse
from app.db.database import get_db
from app.api.routes.auth import get_current_active_user
from app.schemas.auth import User
from app.models.patients import Patient

router = APIRouter()

# CRUD operations
def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Patient).offset(skip).limit(limit).all()

def create_patient(db: Session, patient: PatientCreate):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def update_patient(db: Session, patient_id: int, patient: PatientUpdate):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient:
        for key, value in patient.dict().items():
            setattr(db_patient, key, value)
        db.commit()
        db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient:
        db.delete(db_patient)
        db.commit()
    return db_patient

# API endpoints
@router.post("/", response_model=PatientResponse)
async def create_patient_endpoint(patient: PatientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_patient(db, patient)

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient_endpoint(patient_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.get("/", response_model=List[PatientResponse])
async def get_patients_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return get_patients(db, skip=skip, limit=limit)

@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient_endpoint(patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    updated_patient = update_patient(db, patient_id, patient)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient

@router.delete("/{patient_id}", response_model=PatientResponse)
async def delete_patient_endpoint(patient_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    deleted_patient = delete_patient(db, patient_id)
    if not deleted_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return deleted_patient