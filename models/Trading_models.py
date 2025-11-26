from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class TradingSupportRequest(Base):
    __tablename__ = "trading_support_requests"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email_address = Column(String(200), nullable=False)

    trading_interest = Column(String(200), nullable=False)
    trading_experience = Column(String(200), nullable=False)

    message = Column(Text, nullable=True)
    consent_agreed = Column(Boolean, nullable=False, default=True)

    ip_address = Column(String(100), nullable=True)
    user_agent = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
