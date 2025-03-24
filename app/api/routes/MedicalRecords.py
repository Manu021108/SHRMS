from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from app.api.routes.auth import get_current_active_user
from app.schemas.auth import User

class MedicalRecordBase(BaseModel):
    patient_id: int
    record_date: str
    description: str
    treatment: Optional[str] = None

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecord(MedicalRecordBase):
    id: int

router = APIRouter()

# In-memory storage for medical records
medical_records_db = {}

@router.get("/{medical_record_id}", response_model=MedicalRecord)
async def get_medical_record(medical_record_id: int, current_user: User = Depends(get_current_active_user)):
    medical_record = medical_records_db.get(medical_record_id)
    if not medical_record:
        raise HTTPException(status_code=404, detail="Medical Record not found")
    return medical_record

@router.post("/", response_model=MedicalRecord)
async def create_medical_record(medical_record: MedicalRecordCreate, current_user: User = Depends(get_current_active_user)):
    medical_record_id = len(medical_records_db) + 1
    medical_record_data = MedicalRecord(id=medical_record_id, **medical_record.dict())
    medical_records_db[medical_record_id] = medical_record_data
    return medical_record_data

@router.put("/{medical_record_id}", response_model=MedicalRecord)
async def update_medical_record(medical_record_id: int, medical_record: MedicalRecordCreate, current_user: User = Depends(get_current_active_user)):
    if medical_record_id not in medical_records_db:
        raise HTTPException(status_code=404, detail="Medical Record not found")
    updated_medical_record = MedicalRecord(id=medical_record_id, **medical_record.dict())
    medical_records_db[medical_record_id] = updated_medical_record
    return updated_medical_record

@router.delete("/{medical_record_id}", response_model=MedicalRecord)
async def delete_medical_record(medical_record_id: int, current_user: User = Depends(get_current_active_user)):
    medical_record = medical_records_db.pop(medical_record_id, None)
    if not medical_record:
        raise HTTPException(status_code=404, detail="Medical Record not found")
    return medical_record