from fastapi import APIRouter, Depends, Request, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
import os
from datetime import datetime

from app.core.email_utils import build_email, send_email_message
from app.core.database import get_db
import app.models.Devocation_models as models
import app.schemas.devocation_schema as schemas

router = APIRouter(prefix="/Devocation", tags=["Devocation"])

@router.post("/contact", response_model=schemas.DevocationContactOut, status_code=201)
def submit_devocation_inquiry(
    payload: schemas.DevocationContactCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        # Save to DB
        contact = models.DevocationContact(
            full_name=payload.full_name,
            email=payload.email,
            phone_number=payload.phone_number,
            message=payload.message,
            message_length=len(payload.message),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )

        db.add(contact)
        db.commit()
        db.refresh(contact)

        # Prepare template variables in exact format
        contact_dict = {
            "full_name": contact.full_name,
            "email": contact.email,
            "phone_number": contact.phone_number,
            "message": contact.message,
            "ip_address": contact.ip_address or "127.0.0.1",
            "created_at": contact.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Load template from .env
        template_path = os.getenv("DEVOCATION_EMAIL_TEMPLATE")
        subject = "New Devocation Journey Inquiry"

        # Build and queue email
        msg = build_email(contact_dict, template_path=template_path, subject=subject)
        background_tasks.add_task(send_email_message, msg)

        return contact

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit inquiry: {str(e)}")
