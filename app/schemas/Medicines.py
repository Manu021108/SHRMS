from pydantic import BaseModel, Field

class MedicineBase(BaseModel):
    name: str = Field(..., example="Paracetamol")
    quantity: int = Field(..., gt=0, example=10)

class MedicineIncoming(MedicineBase):
    pass

class MedicineOutgoing(MedicineBase):
    pass

class MedicineCount(BaseModel):
    name: str
    count: int