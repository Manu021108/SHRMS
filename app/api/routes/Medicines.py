from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from app.schemas.Medicines import MedicineIncoming, MedicineOutgoing, MedicineCount
from app.api.routes.auth import get_current_active_user
from app.schemas.auth import User

router = APIRouter()

# In-memory storage for medicine counts
medicine_counts: Dict[str, int] = {}

@router.post("/incoming", response_model=MedicineCount)
async def add_medicine(medicine: MedicineIncoming, current_user: User = Depends(get_current_active_user)):
    if medicine.name in medicine_counts:
        medicine_counts[medicine.name] += medicine.quantity
    else:
        medicine_counts[medicine.name] = medicine.quantity
    return MedicineCount(name=medicine.name, count=medicine_counts[medicine.name])

@router.post("/outgoing", response_model=MedicineCount)
async def remove_medicine(medicine: MedicineOutgoing, current_user: User = Depends(get_current_active_user)):
    if medicine.name not in medicine_counts or medicine_counts[medicine.name] < medicine.quantity:
        raise HTTPException(status_code=400, detail="Not enough medicine in stock")
    medicine_counts[medicine.name] -= medicine.quantity
    return MedicineCount(name=medicine.name, count=medicine_counts[medicine.name])

@router.get("/{medicine_name}", response_model=MedicineCount)
async def get_medicine_count(medicine_name: str, current_user: User = Depends(get_current_active_user)):
    if medicine_name not in medicine_counts:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return MedicineCount(name=medicine_name, count=medicine_counts[medicine_name])