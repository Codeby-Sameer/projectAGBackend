from fastapi import APIRouter, Depends, Request, BackgroundTasks
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.Trading_models import TradingSupportRequest
from schemas.trading_schema import TradingSupportCreate, TradingSupportOut
from core.email_utils import build_email, send_email_message
from jinja2 import Environment, FileSystemLoader
import os

router = APIRouter(prefix="/Wealth", tags=["Wealth"])


# -------------------- DB Dependency --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- Create Request --------------------
@router.post("/submit", response_model=TradingSupportOut, status_code=201)
async def submit_wealth_support_request(
    payload: TradingSupportCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    # Save to DB
    new_request = TradingSupportRequest(
        full_name=payload.full_name,
        phone_number=payload.phone_number,
        email_address=payload.email_address,
        trading_interest=payload.trading_interest,
        trading_experience=payload.trading_experience,
        message=payload.message,
        consent_agreed=payload.consent_agreed,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    # Prepare data for template
    data_dict = {
        "full_name": new_request.full_name,
        "phone_number": new_request.phone_number,
        "email_address": new_request.email_address,
        "trading_interest": new_request.trading_interest,
        "trading_experience": new_request.trading_experience,
        "message": new_request.message,
        "consent_agreed": "Yes" if new_request.consent_agreed else "No",
        "ip_address": new_request.ip_address,
        "created_at": new_request.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # -------------------- Email Template (Preview) --------------------
    env = Environment(loader=FileSystemLoader("app/templates"))
    template_name = os.getenv("TRADING_EMAIL_TEMPLATE", "Trading_email.html")
    template = env.get_template(template_name)
    email_preview = template.render(**data_dict)

    # -------------------- Send Email --------------------
    try:
        msg = build_email(
            data_dict,
            template_path=f"app/templates/{template_name}",
            subject=os.getenv("TRADING_EMAIL_SUBJECT", "📈 New Trading Support Request")
        )
        background_tasks.add_task(send_email_message, msg)
        email_status = "Email sent successfully"
    except Exception as e:
        email_status = f"Email failed: {str(e)}"

    return {
        "status": "success",
        "email_status": email_status,
        "submitted_data": data_dict
    }
