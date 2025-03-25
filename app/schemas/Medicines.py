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

class MedicineResponse(MedicineBase):
    id: int

    class Config:
        orm_mode = True 

class MedicineUpdate(MedicineBase):
    name: str = None
    quantity: int = None                    
class MedicineCreate(MedicineBase):
    pass                