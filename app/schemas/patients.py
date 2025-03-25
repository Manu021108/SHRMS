from pydantic import BaseModel
from typing import Optional

class PatientBase(BaseModel):
    patient_name: str
    age: int
    health_issues: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int

    class Config:
        orm_mode = True