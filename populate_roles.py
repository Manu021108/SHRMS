from sqlalchemy.orm import Session
from app.models.role import Role
from app.db.database import SessionLocal  # Ensure correct import path

def populate_roles():
    db: Session = SessionLocal()

    roles = ["Admin", "Doctor", "Patient"]
    for role_name in roles:
        existing_role = db.query(Role).filter_by(name=role_name).first()
        if not existing_role:
            role = Role(name=role_name)
            db.add(role)

    db.commit()
    db.close()

if __name__ == "__main__":
    populate_roles()
    print("Roles inserted successfully!")