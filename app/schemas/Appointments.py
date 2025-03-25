from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AppointmentBase(BaseModel):
    patient_id: int = Field(..., example=1)
    doctor_id: int = Field(..., example=1)
    appointment_date: datetime = Field(..., example="2023-01-01T10:00:00")
    description: Optional[str] = Field(None, example="Regular check-up")

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    appointment_date: Optional[datetime] = None
    description: Optional[str] = None

class AppointmentInDB(AppointmentBase):
    id: int

class Appointment(AppointmentInDB):
    pass
class AppointmentResponse(AppointmentBase):
    id: int

    class Config:
        orm_mode = True