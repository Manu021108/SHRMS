from pydantic import BaseModel
from typing import Optional

class PrescriptionBase(BaseModel):
    patient_id: int
    doctor_id: int
    medicine_id: int
    dosage: str
    instructions: Optional[str] = None

class PrescriptionCreate(PrescriptionBase):
    pass  # ✅ Ensure this class exists


class PrescriptionUpdate(PrescriptionBase):
    pass

class PrescriptionResponse(PrescriptionBase):
    id: int

    class Config:
        orm_mode = True