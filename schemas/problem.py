from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ProblemReportCreate(BaseModel):
    full_name: str
    primary_phone: str
    email: EmailStr
    existing_client_id: Optional[str] = None
    business_vertical: str
    referring_source: str
    problem_category: str
    priority_level: str
    written_summary: Optional[str] = None


class ProblemReportRead(BaseModel):
    id: int
    full_name: str
    primary_phone: str
    email: EmailStr
    existing_client_id: Optional[str]
    business_vertical: str
    referring_source: str
    problem_category: str
    priority_level: str
    audio_filename: Optional[str]
    written_summary: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
