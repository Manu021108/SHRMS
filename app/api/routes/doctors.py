from fastapi import APIRouter, HTTPException
from app.schemas.doctors import DoctorCreate, DoctorResponse
from app.services import Doctor_Service

router = APIRouter()

@router.post("/", response_model=DoctorResponse)
async def create_doctor(doctor: DoctorCreate):
    return await Doctor_Service.create_doctor(doctor)

@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(doctor_id: int):
    doctor = await Doctor_Service.get_doctor(doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.put("/{doctor_id}", response_model=DoctorResponse)
async def update_doctor(doctor_id: int, doctor: DoctorCreate):
    updated_doctor = await Doctor_Service.update_doctor(doctor_id, doctor)
    if updated_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return updated_doctor

@router.delete("/{doctor_id}", response_model=DoctorResponse)
async def delete_doctor(doctor_id: int):
    deleted_doctor = await Doctor_Service.delete_doctor(doctor_id)
    if deleted_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return deleted_doctor