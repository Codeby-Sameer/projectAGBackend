
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from core.database import Base

class ContactAlternate(Base):
    __tablename__ = "Infra_contacts"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, index=True)
    phone_number = Column(String(50), nullable=True)
    subject = Column(String(300), nullable=True)
    message = Column(Text, nullable=True)
    ip_address = Column(String(100), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
