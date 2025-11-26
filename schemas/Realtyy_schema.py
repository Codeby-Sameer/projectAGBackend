from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

# Tight validation on name, subject length etc.
short_str = constr(strip_whitespace=True, min_length=1, max_length=200)

class ContactCreate(BaseModel):
    full_name: short_str
    email: EmailStr
    phone_number: Optional[constr(strip_whitespace=True, max_length=50)] = None
    property_type: Optional[constr(max_length=100)] = None
    budget_range: Optional[constr(max_length=100)] = None
    timeline: Optional[constr(max_length=100)] = None
    subject: Optional[constr(max_length=300)] = None
    message: Optional[constr(max_length=1000)] = None


class ContactOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    subject: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True  # Pydantic v2 replacement for orm_mode
    }
