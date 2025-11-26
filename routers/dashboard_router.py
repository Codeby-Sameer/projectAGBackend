from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.core.database import get_db
from app.models.problem import Problem
from app.models.appointment import Appointment
from app.models.real_estate import RealEstate

router = APIRouter()


@router.get("/")
def dashboard_overview(db: Session = Depends(get_db)):

    # ---- Problem Stats ----
    total_problems = db.query(func.count(Problem.id)).scalar()
    resolved = db.query(func.count(Problem.id)).filter(Problem.status == "Closed").scalar()
    pending = db.query(func.count(Problem.id)).filter(Problem.status != "Closed").scalar()

    # ---- Appointment Stats ----
    total_appointments = db.query(func.count(Appointment.id)).scalar()

    # ---- Real Estate Stats ----
    total_real_estate = db.query(func.count(RealEstate.id)).scalar()

    # Placeholder satisfaction score
    satisfaction = 94

    # ---- Recent Records ----
    recent_problems = (
        db.query(Problem)
        .order_by(Problem.created_at.desc())
        .limit(5)
        .all()
    )

    recent_appointments = (
        db.query(Appointment)
        .order_by(Appointment.created_at.desc())
        .limit(5)
        .all()
    )

    recent_real_estate = (
        db.query(RealEstate)
        .order_by(RealEstate.created_at.desc())
        .limit(5)
        .all()
    )

    # ---- Unified Activity Feed ----
    activity = []

    # Problems
    for p in recent_problems:
        activity.append({
            "type": "problem",
            "id": p.id,
            "name": p.full_name,
            "title": f"New problem submitted: {p.full_name}",
            "time": p.created_at,
        })

    # Appointments
    for a in recent_appointments:
        activity.append({
            "type": "appointment",
            "id": a.id,
            "name": a.name,
            "title": f"Appointment scheduled with {a.name}",
            "time": a.created_at,
        })

    # Real Estate
    for r in recent_real_estate:
        activity.append({
            "type": "real_estate",
            "id": r.id,
            "name": r.full_name,
            "title": f"New real estate enquiry: {r.full_name}",
            "time": r.created_at,
        })

    # ---- Sort by REAL datetime ----
    activity.sort(key=lambda x: x["time"] if x["time"] else datetime.min, reverse=True)

    # ---- Response ----
    return {
        "stats": {
            "problems": {
                "total": total_problems,
                "resolved": resolved,
                "pending": pending,
            },
            "appointments": {
                "total": total_appointments,
            },
            "real_estate": {
                "total": total_real_estate,
            },
            "satisfaction": satisfaction,
        },
        "recent_activity": activity[:10]
    }
