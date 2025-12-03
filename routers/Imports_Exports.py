import os
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.Imports_Exports_models import Contact
from schemas.imports_Exports_schema import ContactCreate
from core.email_utils import build_email, send_email_message

router = APIRouter(prefix="/imports & Exports", tags=["imports & Exports"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create_contact")
async def submit_imports_exports_contact(data: ContactCreate, request: Request, db: Session = Depends(get_db)):
    # Save to DB
    contact = Contact(**data.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)

    # Send email
    try:
        msg = build_email(data.dict(), template_path=os.getenv("IMPORTS_EXPORTS_EMAIL_TEMPLATE"), subject=os.getenv("IMPORTS_EXPORTS_EMAIL_SUBJECT", "📦 New Imports & Exports Contact Request"))
        send_email_message(msg)
        email_status = "Email sent successfully"
    except Exception as e:
        email_status = f"Email sending failed: {str(e)}"

    # Return ONLY 4 fields
    return {
        "status": "success",
        "email_status": email_status,

        "full_name": data.full_name,
        "email": data.email,
        "phone_number": data.phone_number,
        "message": data.message
    }
