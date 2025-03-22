from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class PatientBase(BaseModel):
    name: str
    email: str
    age : int
    health_issues: str
    phone: str
    address: str
class PatientCreate(PatientBase):
    pass    
class PatientUpdate(PatientBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    health_issues: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class PatientInDB(PatientBase):
    id: int

class Patient(PatientInDB):
    pass    