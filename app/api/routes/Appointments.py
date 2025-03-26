from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.Appointments import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.db.database import get_db
from app.api.routes.auth import get_current_active_user
from app.schemas.auth import User
from app.models.Appointments import Appointment

router = APIRouter()

# CRUD operations
def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()

def get_appointments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Appointment).offset(skip).limit(limit).all()

def create_appointment(db: Session, appointment: AppointmentCreate):
    db_appointment = Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def update_appointment(db: Session, appointment_id: int, appointment: AppointmentUpdate):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if db_appointment:
        for key, value in appointment.dict().items():
            setattr(db_appointment, key, value)
        db.commit()
        db.refresh(db_appointment)
    return db_appointment

def delete_appointment(db: Session, appointment_id: int):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if db_appointment:
        db.delete(db_appointment)
        db.commit()
    return db_appointment

# API endpoints
@router.post("/", response_model=AppointmentResponse)
async def create_appointment_endpoint(appointment: AppointmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_appointment(db, appointment)

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment_endpoint(appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.get("/", response_model=List[AppointmentResponse])
async def get_appointments_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return get_appointments(db, skip=skip, limit=limit)

@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment_endpoint(appointment_id: int, appointment: AppointmentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    updated_appointment = update_appointment(db, appointment_id, appointment)
    if not updated_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return updated_appointment

@router.delete("/{appointment_id}", response_model=AppointmentResponse)
async def delete_appointment_endpoint(appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    deleted_appointment = delete_appointment(db, appointment_id)
    if not deleted_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return deleted_appointment