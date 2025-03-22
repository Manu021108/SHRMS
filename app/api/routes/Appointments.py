from fastapi import APIRouter, HTTPException
from app.schemas.Appointments import AppointmentCreate, AppointmentUpdate, Appointment
from app.services.AppointmentService import AppointmentsService

router = APIRouter()

@router.post("/", response_model=Appointment)
async def create_appointment(appointment: AppointmentCreate):
    return await AppointmentsService.create_appointment(appointment)

@router.get("/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: int):
    appointment = await AppointmentsService.get_appointment(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.put("/{appointment_id}", response_model=Appointment)
async def update_appointment(appointment_id: int, appointment: AppointmentUpdate):
    updated_appointment = await AppointmentsService.update_appointment(appointment_id, appointment)
    if updated_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return updated_appointment

@router.delete("/{appointment_id}", response_model=Appointment)
async def delete_appointment(appointment_id: int):
    deleted_appointment = await AppointmentsService.delete_appointment(appointment_id)
    if deleted_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return deleted_appointment