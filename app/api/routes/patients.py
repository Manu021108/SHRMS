from fastapi import APIRouter
class Patients():
    Patient_id = int
    Patient_name = str
    age = int
    health_issues = str

router = APIRouter()    

@router.get("/patient/{patient_id}")
def get_patient(patient_id: int):
    return {"patient_id": patient_id}
@router.post("/patient/{patient_id}")
def create_patient(patient_id: int):
    return {"patient_id": patient_id}
@router.put("/patient/{patient_id}")
def update_patient(patient_id: int):
    return {"patient_id": patient_id}
@router.delete("/patient/{patient_id}")
def delete_patient(patient_id: int):
    return {"patient_id": patient_id}
