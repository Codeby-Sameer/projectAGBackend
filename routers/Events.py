from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.Events_models import Contact
from schemas.events_schema import ContactCreate
from core.email_utils import build_email, send_email_message


router = APIRouter(prefix="/Events & Media", tags=["Events & Media"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create_contact")
async def create_contact(data: ContactCreate, request: Request, db: Session = Depends(get_db)):
    # Save to DB
    contact = Contact(**data.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)

    # Send email
    try:
        msg = build_email(data.dict(), template_path="templates/events_email.html", subject="📞 New Events & Media Contact Request")
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
