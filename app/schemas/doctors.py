from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class DoctorBase(BaseModel):
    name: str
    email: str
    age : int
    specialisation: str
    phone: str

class DoctorCreate(DoctorBase):
    pass
class DoctorUpdate(DoctorBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    specialisation: Optional[str] = None
    phone: Optional[str] = None

class DoctorInDB(DoctorBase):
    id: int
    class Config:
        orm_mode = True

class DoctorResponse(DoctorBase):
    id: int
    class Config:
        orm_mode = True                