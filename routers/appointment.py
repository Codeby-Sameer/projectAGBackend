# app/routers/appointment_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from schemas.appointment import AppointmentCreate, AppointmentRead
from services.appointment_service import create_appointment, list_appointments, get_appointment_by_id
from core.permissions import role_required

router = APIRouter()

# 🧩 Allowed roles for appointments
ALLOWED_APPOINTMENT_ROLES = ["Administrator", "Admin Personnel", "Manager"]

# ---------------------------------------
# 📅 CREATE Appointment
# ---------------------------------------
@router.post("/", response_model=AppointmentRead, status_code=201)
def create(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    role: str = Depends(role_required(ALLOWED_APPOINTMENT_ROLES))
):
    obj = create_appointment(db, payload)
    return obj

# ---------------------------------------
# 📋 LIST All Appointments
# ---------------------------------------
@router.get("/", response_model=List[AppointmentRead])
def list_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    role: str = Depends(role_required(ALLOWED_APPOINTMENT_ROLES))
):
    return list_appointments(db, skip=skip, limit=limit)

# ---------------------------------------
# 🔍 GET Appointment by ID
# ---------------------------------------
@router.get("/{appointment_id}", response_model=AppointmentRead)
def get_one(
    appointment_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(role_required(ALLOWED_APPOINTMENT_ROLES))
):
    obj = get_appointment_by_id(db, appointment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj