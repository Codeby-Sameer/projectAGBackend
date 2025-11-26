from fastapi import APIRouter, Depends, Request, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.email_utils import build_email, send_email_message
from app.core.database import get_db

from app.models.Trading_models import TradingSupportRequest
from app.schemas.trading_schema import TradingSupportCreate, TradingSupportOut

import os

router = APIRouter(prefix="/trading Support",tags=["Trading Support"])


@router.post("/submit", response_model=TradingSupportOut, status_code=201)
def submit_trading_support_request(
    payload: TradingSupportCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    new_request = TradingSupportRequest(
        full_name=payload.full_name,
        phone_number=payload.phone_number,
        email_address=payload.email_address,
        trading_interest=payload.trading_interest,
        trading_experience=payload.trading_experience,
        message=payload.message,
        consent_agreed=payload.consent_agreed,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    request_dict = {
        "full_name": new_request.full_name,
        "phone_number": new_request.phone_number,
        "email_address": new_request.email_address,
        "trading_interest": new_request.trading_interest,
        "trading_experience": new_request.trading_experience,
        "message": new_request.message,
        "consent_agreed": "Yes" if new_request.consent_agreed else "No",
        "ip_address": new_request.ip_address,
        "created_at": new_request.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }

    template_path = os.getenv("TRADING_EMAIL_TEMPLATE")
    subject = os.getenv("TRADING_EMAIL_SUBJECT", "📈 New Trading Support Request")

    msg = build_email(request_dict, template_path=template_path, subject=subject)
    background_tasks.add_task(send_email_message, msg)

    return new_request
