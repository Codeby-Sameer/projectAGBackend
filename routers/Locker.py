from fastapi import APIRouter, Depends, Request, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
import os

from core.email_utils import build_email, send_email_message
from core.database import get_db
import models.Locker_models as models
import schemas.locker_schema as schemas

router = APIRouter(prefix="/locker", tags=["Locker"])


@router.post("/inquiry", response_model=schemas.LockerInquiryOut, status_code=201)
def submit_locker_inquiry(
    payload: schemas.LockerInquiryCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Submit a new locker inquiry form.
    
    - **full_name**: Full name of the inquirer (2-200 chars, letters only)
    - **email**: Valid email address
    - **phone_number**: +91 format or 10-digit mobile number
    - **locker_size_interest**: One of the predefined locker size options
    - **additional_requirements**: Detailed requirements (10-5000 chars)
    """
    
    # Save to Database
    inquiry = models.LockerInquiry(
        full_name=payload.full_name,
        email=payload.email,
        phone_number=payload.phone_number,
        locker_size_interest=payload.locker_size_interest.value,  # Get enum value
        additional_requirements=payload.additional_requirements,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)

    # Prepare template variables for email
    inquiry_dict = {
        "full_name": inquiry.full_name,
        "email": inquiry.email,
        "phone_number": inquiry.phone_number,
        "locker_size_interest": inquiry.locker_size_interest,
        "additional_requirements": inquiry.additional_requirements,
        "ip_address": inquiry.ip_address,
        "created_at": inquiry.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Load email template configuration from .env
    template_path = os.getenv("LOCKER_EMAIL_TEMPLATE")
    subject = os.getenv("LOCKER_EMAIL_SUBJECT", "New Locker Inquiry Received")

    # Build and queue email in background
    msg = build_email(inquiry_dict, template_path=template_path, subject=subject)
    background_tasks.add_task(send_email_message, msg)

    return inquiry
