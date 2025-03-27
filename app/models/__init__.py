from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import models here
from app.models.patients import Patient
from app.models.doctors import Doctor
from app.models.MedicalRecords import MedicalRecord
from app.models.Appointments import Appointment
from app.models.user import User
from app.models.medicines import Medicine
from app.models.role import Role
from app.models.prescription import Prescription

__all__ = ["Base", "Patient", "Doctor", "MedicalRecord", "Appointment", "User", "Medicine", "Role", "Prescription"]
