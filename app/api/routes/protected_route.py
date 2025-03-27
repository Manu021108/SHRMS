from fastapi import APIRouter, Depends, HTTPException, status
from app.api.routes.auth import check_role, get_current_active_user
from app.schemas.auth import UserResponse
from app.schemas.Medicines import MedicineResponse
from app.schemas.MedicalRecords import MedicalRecordResponse
from app.schemas.patients import PatientResponse
from app.schemas.prescriptions import PrescriptionCreate, PrescriptionResponse
from app.schemas.appointments import AppointmentCreate, AppointmentResponse
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.medicines import Medicine
from app.models.medical_records import MedicalRecord
from app.models.patients import Patient
from app.models.prescriptions import Prescription
from app.models.appointments import Appointment
from typing import List

router = APIRouter()

# ✅ Admin can access everything
@router.get("/admin/all-data", response_model=UserResponse)
async def admin_all_data(current_user: UserResponse = Depends(check_role("admin"))):
    return current_user

# ✅ Doctor Access
@router.get("/doctor/patients", response_model=List[PatientResponse])
async def doctor_patients(db: Session = Depends(get_db), current_user: UserResponse = Depends(check_role("doctor"))):
    patients = db.query(Patient).all()
    return patients

@router.get("/doctor/medicines", response_model=List[MedicineResponse])
async def doctor_medicines(db: Session = Depends(get_db), current_user: UserResponse = Depends(check_role("doctor"))):
    medicines = db.query(Medicine).all()
    return medicines

@router.get("/doctor/medical-records", response_model=List[MedicalRecordResponse])
async def doctor_medical_records(db: Session = Depends(get_db), current_user: UserResponse = Depends(check_role("doctor"))):
    medical_records = db.query(MedicalRecord).all()
    return medical_records

@router.get("/doctor/appointments", response_model=List[AppointmentResponse])
async def doctor_appointments(db: Session = Depends(get_db), current_user: UserResponse = Depends(check_role("doctor"))):
    appointments = db.query(Appointment).all()
    return appointments

# ✅ Patient Access
@router.post("/patient/prescriptions", response_model=PrescriptionResponse)
async def post_prescription(prescription: PrescriptionCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(check_role("patient"))):
    new_prescription = Prescription(**prescription.dict(), patient_id=current_user.id)
    db.add(new_prescription)
    db.commit()
    db.refresh(new_prescription)
    return new_prescription

@router.get("/patient/medical-records", response_model=List[MedicalRecordResponse])
async def patient_medical_records(db: Session = Depends(get_db), current_user: UserResponse = Depends(check_role("patient"))):
    medical_records = db.query(MedicalRecord).filter(MedicalRecord.patient_id == current_user.id).all()
    return medical_records

@router.post("/patient/appointments", response_model=AppointmentResponse)
async def book_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(check_role("patient"))):
    new_appointment = Appointment(**appointment.dict(), patient_id=current_user.id)
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment
