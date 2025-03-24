from fastapi import APIRouter, HTTPException, Depends
from app.schemas.doctors import DoctorCreate, DoctorResponse
from app.services import Doctor_Service
from app.api.routes.auth import get_current_active_user
from app.schemas.auth import User

router = APIRouter()

@router.post("/", response_model=DoctorResponse)
async def create_doctor(doctor: DoctorCreate, current_user: User = Depends(get_current_active_user)):
    return await Doctor_Service.create_doctor(doctor)

@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(doctor_id: int, current_user: User = Depends(get_current_active_user)):
    doctor = await Doctor_Service.get_doctor(doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.put("/{doctor_id}", response_model=DoctorResponse)
async def update_doctor(doctor_id: int, doctor: DoctorCreate, current_user: User = Depends(get_current_active_user)):
    updated_doctor = await Doctor_Service.update_doctor(doctor_id, doctor)
    if updated_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return updated_doctor

@router.delete("/{doctor_id}", response_model=DoctorResponse)
async def delete_doctor(doctor_id: int, current_user: User = Depends(get_current_active_user)):
    deleted_doctor = await Doctor_Service.delete_doctor(doctor_id)
    if deleted_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return deleted_doctor