from fastapi import APIRouter, Depends, HTTPException, status
from app.api.routes.auth import check_role, get_current_active_user
from app.schemas.auth import UserResponse
from app.schemas.Medicines import MedicineResponse
from app.schemas.MedicalRecords import MedicalRecordResponse
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.medicines import Medicine
from app.models.MedicalRecords import MedicalRecord
from typing import List

router = APIRouter()

@router.get("/admin-only", response_model=UserResponse)
async def admin_only_route(current_user: UserResponse = Depends(check_role("admin"))):
    return current_user

@router.get("/doctor-only", response_model=UserResponse)
async def doctor_only_route(current_user: UserResponse = Depends(check_role("doctor"))):
    return current_user

@router.get("/patient-only", response_model=UserResponse)
async def patient_only_route(current_user: UserResponse = Depends(check_role("patient"))):
    return current_user

@router.get("/user-only", response_model=UserResponse)
async def user_only_route(current_user: UserResponse = Depends(check_role("user"))):
    return current_user

@router.get("/doctor/medicines", response_model=List[MedicineResponse])
async def doctor_medicines_route(db: Session = Depends(get_db), current_user: UserResponse = Depends(check_role("doctor"))):
    medicines = db.query(Medicine).all()
    return medicines

@router.get("/doctor/medical-records", response_model=List[MedicalRecordResponse])
async def doctor_medical_records_route(db: Session = Depends(get_db), current_user: UserResponse = Depends(check_role("doctor"))):
    medical_records = db.query(MedicalRecord).all()
    return medical_records

@router.get("/patient/medical-records", response_model=List[MedicalRecordResponse])
async def patient_medical_records_route(db: Session = Depends(get_db), current_user: UserResponse = Depends(check_role("patient"))):
    medical_records = db.query(MedicalRecord).filter(MedicalRecord.patient_id == current_user.id).all()
    return medical_records