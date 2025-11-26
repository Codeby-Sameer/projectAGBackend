from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

short_str = constr(strip_whitespace=True, min_length=1, max_length=200)

class ProjectInquiryCreate(BaseModel):
    full_name: short_str
    email: EmailStr
    phone_number: Optional[str] = None
    project_type: short_str
    vision: constr(strip_whitespace=True, min_length=5, max_length=3000)


class ProjectInquiryOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    project_type: str
    created_at: datetime

    model_config = {"from_attributes": True}
