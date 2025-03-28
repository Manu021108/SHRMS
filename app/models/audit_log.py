from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # Nullable for unauthenticated actions
    action = Column(String, nullable=False)  # e.g., "CREATE", "UPDATE", "DELETE"
    resource = Column(String, nullable=False)  # e.g., "Medicine", "Patient"
    details = Column(Text, nullable=True)  # Additional details about the action
    timestamp = Column(DateTime, default=datetime.utcnow)