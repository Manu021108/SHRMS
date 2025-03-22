from typing import List, Optional
from app.schemas.MedicalRecords import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecord

class RecordsService:
    records = []
    id_counter = 1

    @classmethod
    async def create_record(cls, record: MedicalRecordCreate) -> MedicalRecord:
        new_record = MedicalRecord(id=cls.id_counter, **record.dict())
        cls.records.append(new_record)
        cls.id_counter += 1
        return new_record

    @classmethod
    async def get_record(cls, record_id: int) -> Optional[MedicalRecord]:
        for record in cls.records:
            if record.id == record_id:
                return record
        return None

    @classmethod
    async def update_record(cls, record_id: int, record: MedicalRecordUpdate) -> Optional[MedicalRecord]:
        for idx, existing_record in enumerate(cls.records):
            if existing_record.id == record_id:
                updated_data = record.dict(exclude_unset=True)
                updated_record = existing_record.copy(update=updated_data)
                cls.records[idx] = updated_record
                return updated_record
        return None

    @classmethod
    async def delete_record(cls, record_id: int) -> Optional[MedicalRecord]:
        for idx, existing_record in enumerate(cls.records):
            if existing_record.id == record_id:
                return cls.records.pop(idx)
        return None