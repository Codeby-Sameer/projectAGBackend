from sqlalchemy import Column, Integer, String, Text
from core.database import Base

class Consultation(Base):
    __tablename__ = "wealth_consultations"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100))
    email = Column(String(100))
    phone_number = Column(String(50))

    investment_type = Column(String(100))
    risk_appetite = Column(String(100))
    annual_income = Column(String(100))
    investment_horizon = Column(String(100))
    preferred_contact = Column(String(100))

    subject = Column(String(255))
    message = Column(Text)
