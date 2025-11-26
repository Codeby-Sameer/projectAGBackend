from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ContactCreate(BaseModel):
    full_name: str
    phone_number: str
    message: str

class ContactRead(BaseModel):
    id: int
    full_name: str
    phone: str
    message: str
    created_at: datetime

    model_config = {"from_attributes": True}

