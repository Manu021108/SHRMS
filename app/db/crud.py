from typing import Optional, List
from pymongo import MongoClient
from bson.objectid import ObjectId
from app.core.config import settings
from app.schemas.auth import UserCreate, User
from app.schemas.doctors import DoctorCreate, DoctorResponse
from app.schemas.MedicalRecords import MedicalRecordCreate, MedicalRecord
from app.schemas.Medicines import MedicineIncoming, MedicineOutgoing, MedicineCount
from app.schemas.Appointments import AppointmentCreate, AppointmentUpdate, Appointment

# Connect to MongoDB
client = MongoClient(settings.MONGODB_URI)
db = client[settings.DATABASE_NAME]

# Collections
users_collection = db["users"]
doctors_collection = db["doctors"]
medical_records_collection = db["medical_records"]
medicines_collection = db["medicines"]
appointments_collection = db["appointments"]

# User CRUD operations
def create_user(user: UserCreate) -> User:
    user_dict = user.dict()
    result = users_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return User(**user_dict)

def get_user_by_username(username: str) -> Optional[User]:
    user = users_collection.find_one({"username": username})
    if user:
        return User(**user, id=str(user["_id"]))
    return None

# Doctor CRUD operations
def create_doctor(doctor: DoctorCreate) -> DoctorResponse:
    doctor_dict = doctor.dict()
    result = doctors_collection.insert_one(doctor_dict)
    doctor_dict["id"] = str(result.inserted_id)
    return DoctorResponse(**doctor_dict)

def get_doctor(doctor_id: str) -> Optional[DoctorResponse]:
    doctor = doctors_collection.find_one({"_id": ObjectId(doctor_id)})
    if doctor:
        return DoctorResponse(**doctor, id=str(doctor["_id"]))
    return None

def update_doctor(doctor_id: str, doctor: DoctorCreate) -> Optional[DoctorResponse]:
    doctor_dict = doctor.dict()
    result = doctors_collection.update_one({"_id": ObjectId(doctor_id)}, {"$set": doctor_dict})
    if result.modified_count == 1:
        return get_doctor(doctor_id)
    return None

def delete_doctor(doctor_id: str) -> Optional[DoctorResponse]:
    doctor = doctors_collection.find_one_and_delete({"_id": ObjectId(doctor_id)})
    if doctor:
        return DoctorResponse(**doctor, id=str(doctor["_id"]))
    return None

# Medical Record CRUD operations
def create_medical_record(record: MedicalRecordCreate) -> MedicalRecord:
    record_dict = record.dict()
    result = medical_records_collection.insert_one(record_dict)
    record_dict["id"] = str(result.inserted_id)
    return MedicalRecord(**record_dict)

def get_medical_record(record_id: str) -> Optional[MedicalRecord]:
    record = medical_records_collection.find_one({"_id": ObjectId(record_id)})
    if record:
        return MedicalRecord(**record, id=str(record["_id"]))
    return None

def update_medical_record(record_id: str, record: MedicalRecordCreate) -> Optional[MedicalRecord]:
    record_dict = record.dict()
    result = medical_records_collection.update_one({"_id": ObjectId(record_id)}, {"$set": record_dict})
    if result.modified_count == 1:
        return get_medical_record(record_id)
    return None

def delete_medical_record(record_id: str) -> Optional[MedicalRecord]:
    record = medical_records_collection.find_one_and_delete({"_id": ObjectId(record_id)})
    if record:
        return MedicalRecord(**record, id=str(record["_id"]))
    return None

# Medicine CRUD operations
def add_medicine(medicine: MedicineIncoming) -> MedicineCount:
    medicine_dict = medicine.dict()
    result = medicines_collection.update_one(
        {"name": medicine.name},
        {"$inc": {"quantity": medicine.quantity}},
        upsert=True
    )
    updated_medicine = medicines_collection.find_one({"name": medicine.name})
    return MedicineCount(name=updated_medicine["name"], count=updated_medicine["quantity"])

def remove_medicine(medicine: MedicineOutgoing) -> MedicineCount:
    medicine_dict = medicine.dict()
    result = medicines_collection.update_one(
        {"name": medicine.name, "quantity": {"$gte": medicine.quantity}},
        {"$inc": {"quantity": -medicine.quantity}}
    )
    if result.modified_count == 0:
        raise ValueError("Not enough medicine in stock")
    updated_medicine = medicines_collection.find_one({"name": medicine.name})
    return MedicineCount(name=updated_medicine["name"], count=updated_medicine["quantity"])

def get_medicine_count(medicine_name: str) -> Optional[MedicineCount]:
    medicine = medicines_collection.find_one({"name": medicine_name})
    if medicine:
        return MedicineCount(name=medicine["name"], count=medicine["quantity"])
    return None

# Appointment CRUD operations
def create_appointment(appointment: AppointmentCreate) -> Appointment:
    appointment_dict = appointment.dict()
    result = appointments_collection.insert_one(appointment_dict)
    appointment_dict["id"] = str(result.inserted_id)
    return Appointment(**appointment_dict)

def get_appointment(appointment_id: str) -> Optional[Appointment]:
    appointment = appointments_collection.find_one({"_id": ObjectId(appointment_id)})
    if appointment:
        return Appointment(**appointment, id=str(appointment["_id"]))
    return None

def update_appointment(appointment_id: str, appointment: AppointmentUpdate) -> Optional[Appointment]:
    appointment_dict = appointment.dict()
    result = appointments_collection.update_one({"_id": ObjectId(appointment_id)}, {"$set": appointment_dict})
    if result.modified_count == 1:
        return get_appointment(appointment_id)
    return None

def delete_appointment(appointment_id: str) -> Optional[Appointment]:
    appointment = appointments_collection.find_one_and_delete({"_id": ObjectId(appointment_id)})
    if appointment:
        return Appointment(**appointment, id=str(appointment["_id"]))
    return None