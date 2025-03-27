from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.prescription import PrescriptionCreate, PrescriptionUpdate, PrescriptionResponse
from app.db.database import get_db
from app.models.prescription import Prescription
from app.api.routes.auth import get_current_active_user
from app.schemas.auth import User

router = APIRouter()

@router.post("/", response_model=PrescriptionResponse)
async def create_prescription(
    prescription: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_prescription = Prescription(**prescription.dict())
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

@router.get("/{prescription_id}", response_model=PrescriptionResponse)
async def get_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription

@router.get("/", response_model=List[PrescriptionResponse])
async def get_prescriptions(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    prescriptions = db.query(Prescription).offset(skip).limit(limit).all()
    return prescriptions

@router.put("/{prescription_id}", response_model=PrescriptionResponse)
async def update_prescription(
    prescription_id: int,
    prescription: PrescriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not db_prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    for key, value in prescription.dict().items():
        setattr(db_prescription, key, value)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

@router.delete("/{prescription_id}", response_model=PrescriptionResponse)
async def delete_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not db_prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    db.delete(db_prescription)
    db.commit()
    return db_prescription