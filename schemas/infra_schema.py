from datetime import datetime
from pydantic import BaseModel, EmailStr, constr
from typing import Optional

short_str = constr(strip_whitespace=True, min_length=1, max_length=200)

class ContactAlternateCreate(BaseModel):
    full_name: short_str
    email: EmailStr
    phone_number: Optional[constr(strip_whitespace=True, max_length=50)] = None
    subject: Optional[constr(max_length=300)] = None
    message: Optional[constr(max_length=2000)] = None

class ContactAlternateOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    subject: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
