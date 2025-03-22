from fastapi import APIRouter, HTTPException
from app.schemas.MedicalRecords import MedicalRecordCreate, MedicalRecord
from app.services import RecordsService


router = APIRouter()

@router.post("/", response_model=MedicalRecord)
async def create_medical_record(medical_record: MedicalRecordCreate):
    return await RecordsService.create_medical_record(medical_record)

@router.get("/{medical_record_id}", response_model=MedicalRecord)
async def get_medical_record(medical_record_id: int):
    medical_record = await RecordsService.get_medical_record(medical_record_id)
    if medical_record is None:
        raise HTTPException(status_code=404, detail="Medical Record not found")
    return medical_record

@router.put("/{medical_record_id}", response_model=MedicalRecord)
async def update_medical_record(medical_record_id: int, medical_record: MedicalRecordCreate):
    updated_medical_record = await RecordsService.update_medical_record(medical_record_id, medical_record)
    if updated_medical_record is None:
        raise HTTPException(status_code=404, detail="Medical Record not found")
    return updated_medical_record

@router.delete("/{medical_record_id}", response_model=MedicalRecord)
async def delete_medical_record(medical_record_id: int):
    deleted_medical_record = await RecordsService.delete_medical_record(medical_record_id)
    if deleted_medical_record is None:
        raise HTTPException(status_code=404, detail="Medical Record not found")
    return deleted_medical_record