import os
from fastapi import APIRouter, Request, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from typing import Dict
from core.database import get_db
import models.Infra_models as models
import schemas.infra_schema as schemas
from core.email_utils import build_email, send_email_message

router = APIRouter(prefix="/Infra", tags=["Infra"])

@router.post("/", response_model=schemas.ContactAlternateOut, status_code=201)
def submit_infra_contact(
    payload: schemas.ContactAlternateCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    contact = models.ContactAlternate(
        full_name=payload.full_name,
        email=payload.email,
        phone_number=payload.phone_number,
        subject=payload.subject,
        message=payload.message,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)

    # prepare dict for template injection
    contact_dict: Dict = {
        "full_name": contact.full_name,
        "email": contact.email,
        "phone_number": contact.phone_number,
        "subject": contact.subject,
        "message": contact.message,
        "ip_address": contact.ip_address,
    }

    # send email using alternate template and subject (env or pass directly)
    # If you want a different subject/template set env vars: ALT_EMAIL_SUBJECT, ALT_EMAIL_TEMPLATE
    msg = build_email(contact_dict,
                                           template_path=os.getenv("ALT_EMAIL_TEMPLATE"),
                                           subject=os.getenv("ALT_EMAIL_SUBJECT"))
    background_tasks.add_task(send_email_message, msg)

    return contact
