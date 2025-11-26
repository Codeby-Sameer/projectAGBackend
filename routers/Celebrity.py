from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
import traceback
from typing import List, Dict, Any

from app.core.database import get_db
from app.models.Celebrity_models import Message
from app.schemas.yatra_schema import ContactCreate, ContactRead
from app.core.email_utils import build_email, send_email_message

router = APIRouter(prefix="/Celebrity", tags=["Celebrity"])


@router.post("/create", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
def create_contact(
    payload: ContactCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    msg = Message(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone_number,
        message=payload.message,
    )

    db.add(msg)
    try:
        db.commit()
        db.refresh(msg)
    except Exception:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Database error")

    contact_dict: Dict[str, Any] = {
        "full_name": getattr(msg, "full_name", "") or "",
        "email": getattr(msg, "email", "") or "",
        "phone_number": getattr(msg, "phone", "") or "",
        "message": getattr(msg, "message", "") or "",
        "id": getattr(msg, "id", None),
        "created_at": getattr(msg, "created_at", None).isoformat() if getattr(msg, "created_at", None) else "",
    }

    try:
        email_msg = build_email(contact_dict)
        if email_msg:
            background_tasks.add_task(send_email_message, email_msg)
    except Exception:
        traceback.print_exc()

    return msg