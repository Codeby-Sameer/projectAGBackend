from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import datetime

short_str = constr(strip_whitespace=True, min_length=1, max_length=200)
phone_str = constr(strip_whitespace=True, min_length=7, max_length=20)
long_text = constr(strip_whitespace=True, min_length=1, max_length=2000)

class TradingSupportCreate(BaseModel):
    full_name: short_str
    phone_number: phone_str
    email_address: EmailStr
    trading_interest: short_str
    trading_experience: short_str
    message: Optional[long_text] = None
    consent_agreed: bool = True

class TradingSupportOut(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email_address: EmailStr
    trading_interest: str
    trading_experience: str
    message: Optional[str]
    consent_agreed: bool
    created_at: datetime

    model_config = {"from_attributes": True}
