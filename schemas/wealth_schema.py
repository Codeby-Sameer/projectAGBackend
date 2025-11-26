from pydantic import BaseModel, EmailStr

class ConsultationRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    investment_type: str
    risk_appetite: str
    annual_income: str
    investment_horizon: str
    preferred_contact: str
    subject: str
    message: str

    class Config:
        orm_mode = True
