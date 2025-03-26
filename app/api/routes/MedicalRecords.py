from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.MedicalRecords import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse
from app.db.database import get_db
from app.api.routes.auth import get_current_active_user
from app.schemas.auth import User
from app.models.MedicalRecords import MedicalRecord

router = APIRouter()

# CRUD operations
def get_medical_record(db: Session, medical_record_id: int):
    return db.query(MedicalRecord).filter(MedicalRecord.id == medical_record_id).first()

def get_medical_records(db: Session, skip: int = 0, limit: int = 10):
    return db.query(MedicalRecord).offset(skip).limit(limit).all()

def create_medical_record(db: Session, medical_record: MedicalRecordCreate):
    db_medical_record = MedicalRecord(**medical_record.dict())
    db.add(db_medical_record)
    db.commit()
    db.refresh(db_medical_record)
    return db_medical_record

def update_medical_record(db: Session, medical_record_id: int, medical_record: MedicalRecordUpdate):
    db_medical_record = db.query(MedicalRecord).filter(MedicalRecord.id == medical_record_id).first()
    if db_medical_record:
        for key, value in medical_record.dict().items():
            setattr(db_medical_record, key, value)
        db.commit()
        db.refresh(db_medical_record)
    return db_medical_record

def delete_medical_record(db: Session, medical_record_id: int):
    db_medical_record = db.query(MedicalRecord).filter(MedicalRecord.id == medical_record_id).first()
    if db_medical_record:
        db.delete(db_medical_record)
        db.commit()
    return db_medical_record

# API endpoints
@router.post("/", response_model=MedicalRecordResponse)
async def create_medical_record_endpoint(medical_record: MedicalRecordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_medical_record(db, medical_record)

@router.get("/{medical_record_id}", response_model=MedicalRecordResponse)
async def get_medical_record_endpoint(medical_record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    medical_record = get_medical_record(db, medical_record_id)
    if not medical_record:
        raise HTTPException(status_code=404, detail="Medical Record not found")
    return medical_record

@router.get("/", response_model=List[MedicalRecordResponse])
async def get_medical_records_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return get_medical_records(db, skip=skip, limit=limit)

@router.put("/{medical_record_id}", response_model=MedicalRecordResponse)
async def update_medical_record_endpoint(medical_record_id: int, medical_record: MedicalRecordUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    updated_medical_record = update_medical_record(db, medical_record_id, medical_record)
    if not updated_medical_record:
        raise HTTPException(status_code=404, detail="Medical Record not found")
    return updated_medical_record

@router.delete("/{medical_record_id}", response_model=MedicalRecordResponse)
async def delete_medical_record_endpoint(medical_record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    deleted_medical_record = delete_medical_record(db, medical_record_id)
    if not deleted_medical_record:
        raise HTTPException(status_code=404, detail="Medical Record not found")
    return deleted_medical_record