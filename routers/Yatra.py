from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from core.database import get_db
from models.Yatra_models import Message
from schemas.yatra_schema import ContactCreate, ContactRead
from core.email_utils import build_email, send_email_message

router = APIRouter(prefix="/Yatra", tags=["Yatra"])


@router.post("/create", response_model=ContactRead, status_code=201)
def create_contact(
    payload: ContactCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    msg = Message(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone_number,
        message=payload.message
    )

    db.add(msg)
    db.commit()
    db.refresh(msg)

    contact_dict = {
        "full_name": msg.full_name,
        "email": msg.email,
        "phone_number": msg.phone,
        "message": msg.message,
        "id": msg.id,
        "created_at": msg.created_at.isoformat() if msg.created_at else "",
    }

    email_msg = build_email(contact_dict)
    background_tasks.add_task(send_email_message, email_msg)

    return msg

