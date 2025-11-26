from pydantic import BaseModel, EmailStr

class ContactCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    message: str

    class Config:
        orm_mode = True
