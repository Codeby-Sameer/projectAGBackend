from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Optional
from datetime import datetime

class DevocationContactCreate(BaseModel):
    full_name: constr(strip_whitespace=True, min_length=1, max_length=200)
    email: EmailStr
    phone_number: constr(strip_whitespace=True, min_length=10, max_length=15)
    message: constr(strip_whitespace=True, min_length=1, max_length=1000)
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v):
        # Basic phone number validation
        if not v.replace('+', '').replace(' ', '').replace('(', '').replace(')', '').replace('-', '').isdigit():
            raise ValueError('Phone number must contain only digits and valid symbols')
        return v

class DevocationContactOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone_number: str
    message_length: int
    created_at: datetime

    model_config = {"from_attributes": True}