from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.medicine import MedicineCreate, MedicineUpdate, MedicineResponse
from app.crud.medicine import get_medicine, get_medicines, create_medicine, update_medicine, delete_medicine
from app.db.database import get_db
from app.api.routes.auth import get_current_active_user
from app.schemas.auth import User

router = APIRouter()

@router.post("/", response_model=MedicineResponse)
async def create_medicine_endpoint(medicine: MedicineCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_medicine(db, medicine)

@router.get("/{medicine_id}", response_model=MedicineResponse)
async def get_medicine_endpoint(medicine_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    medicine = get_medicine(db, medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

@router.get("/", response_model=List[MedicineResponse])
async def get_medicines_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return get_medicines(db, skip=skip, limit=limit)

@router.put("/{medicine_id}", response_model=MedicineResponse)
async def update_medicine_endpoint(medicine_id: int, medicine: MedicineUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    updated_medicine = update_medicine(db, medicine_id, medicine)
    if not updated_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return updated_medicine

@router.delete("/{medicine_id}", response_model=MedicineResponse)
async def delete_medicine_endpoint(medicine_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    deleted_medicine = delete_medicine(db, medicine_id)
    if not deleted_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return deleted_medicine