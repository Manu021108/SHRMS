from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from app.api.routes.auth import get_current_active_user
from app.schemas.auth import User

class Patient(BaseModel):
    patient_id: int
    patient_name: str
    age: int
    health_issues: Optional[str] = None

router = APIRouter()

# In-memory storage for patients
patients_db = {}

@router.get("/patient/{patient_id}", response_model=Patient)
async def get_patient(patient_id: int, current_user: User = Depends(get_current_active_user)):
    patient = patients_db.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/patient/", response_model=Patient)
async def create_patient(patient: Patient, current_user: User = Depends(get_current_active_user)):
    if patient.patient_id in patients_db:
        raise HTTPException(status_code=400, detail="Patient already exists")
    patients_db[patient.patient_id] = patient
    return patient

@router.put("/patient/{patient_id}", response_model=Patient)
async def update_patient(patient_id: int, patient: Patient, current_user: User = Depends(get_current_active_user)):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    patients_db[patient_id] = patient
    return patient

@router.delete("/patient/{patient_id}", response_model=Patient)
async def delete_patient(patient_id: int, current_user: User = Depends(get_current_active_user)):
    patient = patients_db.pop(patient_id, None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient