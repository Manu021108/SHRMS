from fastapi import APIRouter, Depends, HTTPException, status
from app.api.routes.auth import check_role, get_current_active_user
from app.schemas.auth import UserResponse
from app.schemas.Medicines import MedicineResponse
from app.schemas.MedicalRecords import MedicalRecordResponse
from app.schemas.patients import PatientResponse
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse
from app.schemas.Appointments import AppointmentCreate, AppointmentResponse
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.medicines import Medicine
from app.models.MedicalRecords import MedicalRecord
from app.models.patients import Patient
from app.models.prescription import Prescription
from app.models.Appointments import Appointment
from typing import List
from app.models.doctors import Doctor

router = APIRouter()

@router.get("/doctor/medical-records", response_model=List[MedicalRecordResponse])
async def doctor_medical_records_route(
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(check_role("doctor"))
):
    # ✅ Doctors can only see medical records
    medical_records = db.query(MedicalRecord).all()
    return medical_records

@router.get("/doctor/patients", response_model=List[PatientResponse])
async def doctor_patients_route(
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(check_role("doctor"))
):
    # ✅ Doctors can only view patients
    patients = db.query(Patient).all()
    return patients

@router.get("/doctor/medicines", response_model=List[MedicineResponse])
async def doctor_medicines_route(
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(check_role("doctor"))
):
    # ✅ Doctors can only see medicine availability
    medicines = db.query(Medicine).all()
    return medicines

@router.get("/doctor/appointments", response_model=List[AppointmentResponse])
async def doctor_appointments_route(
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(check_role("doctor"))
):
    # ✅ Doctors can only see appointments
    appointments = db.query(Appointment).all()
    return appointments
@router.post("/patient/prescriptions", response_model=PrescriptionResponse)
async def patient_create_prescription(
    prescription: PrescriptionCreate,
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(check_role("patient"))
):
    # ✅ Patients can only create prescriptions
    new_prescription = Prescription(**prescription.dict(), patient_id=current_user.id)
    db.add(new_prescription)
    db.commit()
    db.refresh(new_prescription)
    return new_prescription

@router.get("/patient/medical-records", response_model=List[MedicalRecordResponse])
async def patient_medical_records_route(
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(check_role("patient"))
):
    # ✅ Patients can only see their own medical records
    medical_records = db.query(MedicalRecord).filter(MedicalRecord.patient_id == current_user.id).all()
    return medical_records

@router.post("/patient/appointments", response_model=AppointmentResponse)
async def patient_book_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(check_role("patient"))
):
    # ✅ Patients can book appointments
    new_appointment = Appointment(**appointment.dict(), patient_id=current_user.id)
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment
@router.get("/admin/all-data", response_model=dict)
async def admin_view_all(
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(check_role("admin"))
):
    # ✅ Admins can access everything
    data = {
        "patients": db.query(Patient).all(),
        "doctors": db.query(Doctor).all(),
        "medical_records": db.query(MedicalRecord).all(),
        "prescriptions": db.query(Prescription).all(),
        "appointments": db.query(Appointment).all(),
        "medicines": db.query(Medicine).all(),
    }
    return data
