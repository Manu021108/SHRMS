from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from loguru import logger

def log_audit_event(
    db: Session,
    user_id: int | None,
    action: str,
    resource: str,
    details: str | None = None,
):
    """
    Logs an audit event to the database.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int | None): ID of the user performing the action (nullable for unauthenticated actions).
        action (str): The action performed (e.g., "CREATE", "UPDATE", "DELETE").
        resource (str): The resource affected (e.g., "Medicine", "Patient").
        details (str | None): Additional details about the action (optional).
    """
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            details=details,
        )
        db.add(audit_log)
        db.commit()
        logger.info(f"Audit log created: {action} on {resource} by user {user_id}")
    except Exception as e:
        logger.error(f"Failed to log audit event: {e}")