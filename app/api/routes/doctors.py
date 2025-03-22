from fastapi import APIRouter
from app.schemas.doctors import DoctorCreate, DoctorResponse
from app.services import DoctorService

router = APIRouter()

@router.get("/", response_model=[DoctorResponse])
async def CreateDoctor(doctor: DoctorCreate):
    return await DoctorService.create_doctor(doctor)
