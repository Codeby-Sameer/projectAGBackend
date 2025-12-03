from fastapi import APIRouter, Depends, Request, BackgroundTasks
from sqlalchemy.orm import Session
from schemas.Realtyy_schema import ContactCreate,ContactOut
from models.Realtyy_models import Contact
from core.database import get_db
from core.email_utils import build_email, send_email_message


router = APIRouter(prefix="/Realtyy", tags=["Realtyy"])


@router.post("/", response_model=ContactOut)
def Realtyy_contact(
    payload: ContactCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    contact = Contact(
        full_name=payload.full_name,
        email=payload.email,
        phone_number=payload.phone_number,
        property_type=payload.property_type,
        budget_range=payload.budget_range,
        timeline=payload.timeline,
        subject=payload.subject,
        message=payload.message,
        ip_address=request.client.host
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    # Prepare email data
    contact_dict = {
        "full_name": contact.full_name,
        "email": contact.email,
        "phone_number": contact.phone_number,
        "property_type": contact.property_type,
        "budget_range": contact.budget_range,
        "timeline": contact.timeline,
        "subject": contact.subject,
        "message": contact.message,
        "ip_address": contact.ip_address,
    }

    # Send email in background
    msg = build_email(contact_dict)
    background_tasks.add_task(send_email_message, msg)

    return contact
