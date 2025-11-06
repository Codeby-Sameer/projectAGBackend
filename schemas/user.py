 
#user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
 
 
class UserBase(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str] = "staff"
    is_active: Optional[bool] = True
 
 
class UserCreate(UserBase):
    password: str
 
 
class UserUpdate(UserBase):
    password: Optional[str] = None
 
 
class UserRead(UserBase):
    id: int
    created_at: Optional[datetime]
 
    class Config:
        from_attributes = True  # ✅ for Pydantic v2
 