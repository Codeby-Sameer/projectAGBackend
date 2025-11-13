from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
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

    # ---- Build Unified Activity Feed ----
    activity = []

    # Problem Activity
    for p in recent_problems:
        activity.append({
            "type": "problem",
            "title": f"New problem submitted: {p.full_name}",
            "time": p.created_at,
        })

    # Appointment Activity
    for a in recent_appointments:
        activity.append({
            "type": "appointment",
            "title": f"Appointment scheduled with {a.name}",
            "time": a.created_at,
        })

    # ---- FIX: Normalize timestamps before sorting ----
    for item in activity:
        t = item["time"]
        # Convert both naive and aware datetimes into sortable ISO format
        item["time"] = t.isoformat() if hasattr(t, "isoformat") else str(t)

    # Safe sort by most recent
    activity = sorted(activity, key=lambda x: x["time"], reverse=True)

    # ---- Response ----
    return {
        "stats": {
            "total_problems": total_problems,
            "resolved": resolved,
            "pending": pending,
            "satisfaction": satisfaction,
        },
        "recent_activity": activity[:10]
    }
