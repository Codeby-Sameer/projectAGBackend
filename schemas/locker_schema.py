from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
import re

# Enum for Locker Size Options
class LockerSizeEnum(str, Enum):
    SMALL = "Small (Documents, Jewelry)"
    MEDIUM = "Medium (Electronics, Important Files)"
    LARGE = "Large (Business Assets, Family Heirlooms)"
    CUSTOM = "Custom Size Requirements"
    NOT_SURE = "Not Sure - Need Guidance"


# String constraints
short_str = constr(strip_whitespace=True, min_length=1, max_length=200)


class LockerInquiryCreate(BaseModel):
    full_name: short_str
    email: EmailStr
    phone_number: str
    locker_size_interest: LockerSizeEnum
    additional_requirements: constr(strip_whitespace=True, min_length=10, max_length=5000)

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        # Remove all spaces and hyphens for validation
        cleaned = v.strip().replace(" ", "").replace("-", "")
        
        # Check for +91 format (e.g., +91 9876543210 or +919876543210)
        if cleaned.startswith("+91"):
            phone_digits = cleaned[3:]
            if len(phone_digits) == 10 and phone_digits.isdigit():
                return v
            else:
                raise ValueError("Phone number after +91 must be exactly 10 digits")
        
        # Check for standard 10-digit format (e.g., 9876543210)
        elif len(cleaned) == 10 and cleaned.isdigit():
            return v
        
        else:
            raise ValueError(
                "Phone number must be in +91XXXXXXXXXX format or 10-digit mobile number"
            )

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        if len(v.strip()) < 2:
            raise ValueError("Full name must be at least 2 characters long")
        if not re.match(r'^[a-zA-Z\s.]+$', v):
            raise ValueError("Full name can only contain letters, spaces, and dots")
        return v.strip()


class LockerInquiryOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone_number: str
    locker_size_interest: str
    created_at: datetime

    model_config = {"from_attributes": True}