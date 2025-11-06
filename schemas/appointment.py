from pydantic import BaseModel, Field
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime

base_model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class AppointmentBase(BaseModel):
    model_config = base_model_config

    name: str = Field(..., min_length=2)
    email: str = Field()
    phone: str = Field()
    department: str = Field(..., min_length=1)
    date: str = Field(...)
    time: str = Field(...)
    message: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentRead(AppointmentBase):
    id: int
    created_at: datetime
