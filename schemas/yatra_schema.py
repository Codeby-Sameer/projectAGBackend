from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional

short_str = constr(strip_whitespace=True, min_length=1, max_length=200)

class ContactCreate(BaseModel):
    full_name: short_str
    email: EmailStr
    phone_number: Optional[str] = None
    message: Optional[str] = None


class ContactRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    message: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
