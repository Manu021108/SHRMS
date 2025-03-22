from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class MedicalRecordBase(BaseModel):
    patient_id: int = Field(..., example=1)
    record_date: date = Field(..., example="2023-01-01")
    description: str = Field(..., example="Annual check-up")
    treatment: Optional[str] = Field(None, example="Prescribed medication X")

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(MedicalRecordBase):
    patient_id: Optional[int] = None
    record_date: Optional[date] = None
    description: Optional[str] = None
    treatment: Optional[str] = None

class MedicalRecordInDB(MedicalRecordBase):
    id: int

class MedicalRecord(MedicalRecordInDB):
    pass