from fastapi import APIRouter, Depends, Request, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
import os

from app.core.email_utils import build_email, send_email_message
from app.core.database import get_db
import app.models.Technology_models as models
import app.schemas.Technology_schema as schemas

router = APIRouter(prefix="/Technology & Safety", tags=["Technology & Safety"])

@router.post("/contact", response_model=schemas.AnandContactOut, status_code=201)
def submit_anand_contact(
    payload: schemas.AnandContactCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Save to DB
    contact = models.AnandContact(
        full_name=payload.full_name,
        email=payload.email,
        phone_number=payload.phone_number,
        message=payload.message,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    # Prepare template variables
    contact_dict = {
        "full_name": contact.full_name,
        "email": contact.email,
        "phone_number": contact.phone_number or "Not provided",
        "message": contact.message,
        "ip_address": contact.ip_address,
    }

    # Load template from .env
    template_path = os.getenv("ANAND_EMAIL_TEMPLATE")
    subject = os.getenv("EMAIL_SUBJECT", "New Contact Form Submission - Anand Technology & Safety")

    # Build and queue email
    msg = build_email(contact_dict, template_path=template_path, subject=subject)
    background_tasks.add_task(send_email_message, msg)

    return contact