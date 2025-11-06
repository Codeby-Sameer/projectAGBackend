from sqlalchemy.orm import Session
from app.schemas.appointment import AppointmentCreate
from app.models.appointment import Appointment

def create_appointment(db: Session, payload: AppointmentCreate) -> Appointment:
    obj = Appointment(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        department=payload.department,
        date=payload.date,
        time=payload.time,
        message=payload.message
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_appointment_by_id(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()

def list_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Appointment).offset(skip).limit(limit).all()
