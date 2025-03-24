from fastapi import FastAPI
from typing import Union
from fastapi.responses import JSONResponse
from app.api.routes import patients, doctors, MedicalRecords, Medicines, Appointments, auth
from pymongo import MongoClient
from app.core.config import settings
from fastapi.exceptions import HTTPException



app = FastAPI(title="Swecha Health Records System (SHRS)", version="1.0.0")
# Connect to MongoDB
client = MongoClient(settings.MONGODB_URI)
db = client[settings.DATABASE_NAME]


app.include_router(patients.router, prefix="/Patients", tags=["patients"])
app.include_router(doctors.router, prefix="/Doctors", tags=["doctors"])
app.include_router(MedicalRecords.router, prefix="/MedicalRecords", tags=["MedicalRecords"])
app.include_router(Medicines.router, prefix="/Medicines", tags=["Medicines"])
app.include_router(Appointments.router, prefix="/Appointments", tags=["Appointments"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


app.get("/")
async def root():
    return {"message": "Welcome to the Swecha Health Records System (SHRS)"}