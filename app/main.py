from fastapi import FastAPI
from typing import Union
from fastapi.responses import JSONResponse
from app.api.routes import patients, doctors, MedicalRecords, Medicines



app = FastAPI(title="Swecha Health Records System (SHRS)", version="1.0.0")

app.include_router(patients.router, prefix="/Patients", tags=["patients"])
app.include_router(doctors.router, prefix="/Doctors", tags=["doctors"])
app.include_router(MedicalRecords.router, prefix="/MedicalRecords", tags=["MedicalRecords"])
app.include_router(Medicines.router, prefix="/Medicines", tags=["Medicines"])

