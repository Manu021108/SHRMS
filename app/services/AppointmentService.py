from typing import List, Optional
from app.schemas.Appointments import AppointmentCreate, AppointmentUpdate, Appointment

class AppointmentsService:
    appointments = []
    id_counter = 1

    @classmethod
    async def create_appointment(cls, appointment: AppointmentCreate) -> Appointment:
        new_appointment = Appointment(id=cls.id_counter, **appointment.dict())
        cls.appointments.append(new_appointment)
        cls.id_counter += 1
        return new_appointment

    @classmethod
    async def get_appointment(cls, appointment_id: int) -> Optional[Appointment]:
        for appointment in cls.appointments:
            if appointment.id == appointment_id:
                return appointment
        return None

    @classmethod
    async def update_appointment(cls, appointment_id: int, appointment: AppointmentUpdate) -> Optional[Appointment]:
        for idx, existing_appointment in enumerate(cls.appointments):
            if existing_appointment.id == appointment_id:
                updated_data = appointment.dict(exclude_unset=True)
                updated_appointment = existing_appointment.copy(update=updated_data)
                cls.appointments[idx] = updated_appointment
                return updated_appointment
        return None

    @classmethod
    async def delete_appointment(cls, appointment_id: int) -> Optional[Appointment]:
        for idx, existing_appointment in enumerate(cls.appointments):
            if existing_appointment.id == appointment_id:
                return cls.appointments.pop(idx)
        return None