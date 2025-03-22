import sys
sys.path.append('.')
class DoctorService:
    def __init__(self, doctor_repo):
        self.doctor_repo = doctor_repo

    def get_doctors(self):
        return self.doctor_repo.get_doctors()

    def get_doctor_by_id(self, doctor_id):
        return self.doctor_repo.get_doctor_by_id(doctor_id)

    def create_doctor(self, doctor):
        return self.doctor_repo.create_doctor(doctor)

    def update_doctor(self, doctor_id, doctor):
        return self.doctor_repo.update_doctor(doctor_id, doctor)

    def delete_doctor(self, doctor_id):
        return self.doctor_repo.delete_doctor(doctor_id)