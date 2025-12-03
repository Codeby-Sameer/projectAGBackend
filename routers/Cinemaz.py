from fastapi import APIRouter, Depends, Request, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
import os
from core.email_utils import build_email, send_email_message
from core.database import get_db
import models.Cinemaz_models as models
import schemas.Cinemaz_schema as schemas

router = APIRouter(prefix="/Cinemaz", tags=["Cinemaz"])


@router.post("/", response_model=schemas.ProjectInquiryOut, status_code=201)
def submit_cinemaz_inquiry(
    payload: schemas.ProjectInquiryCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Save to DB
    inquiry = models.ProjectInquiry(
        full_name=payload.full_name,
        email=payload.email,
        phone_number=payload.phone_number,
        project_type=payload.project_type,
        vision=payload.vision,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)

    # Prepare template variables
    inquiry_dict = {
        "full_name": inquiry.full_name,
        "email": inquiry.email,
        "phone_number": inquiry.phone_number,
        "project_type": inquiry.project_type,
        "vision": inquiry.vision,
        "ip_address": inquiry.ip_address,
    }

    # Load alt template from .env
    template_path = os.getenv("PROJECT_EMAIL_TEMPLATE")
    subject = os.getenv("PROJECT_EMAIL_SUBJECT", "New Project Inquiry Received")

    # Build and queue email
    msg = build_email(inquiry_dict, template_path=template_path, subject=subject)
    background_tasks.add_task(send_email_message, msg)

    return inquiry
