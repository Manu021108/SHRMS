from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.api.routes import patients, doctors, MedicalRecords, Medicines, Appointments, auth
from app.core.config import settings
from app.core.security import decode_access_token
from app.db.database import SessionLocal, engine, Base
from app.models import patient  # Import your models here

# FastAPI app instance
app = FastAPI(title="Swecha Health Records System (SHRS)", version="1.0.0")

# Initialize the database
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Middleware to enforce authentication
async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        return payload  # Return decoded user information
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Include routers
app.include_router(patients.router, prefix="/Patients", tags=["patients"])
app.include_router(doctors.router, prefix="/Doctors", tags=["doctors"])
app.include_router(MedicalRecords.router, prefix="/MedicalRecords", tags=["MedicalRecords"])
app.include_router(Medicines.router, prefix="/Medicines", tags=["Medicines"])
app.include_router(Appointments.router, prefix="/Appointments", tags=["appointments"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Swecha Health Records System (SHRS)"}