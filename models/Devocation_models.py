from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from core.database import Base

class DevocationContact(Base):
    __tablename__ = "devocation_contacts"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, index=True)
    phone_number = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    message_length = Column(Integer, nullable=False)

    ip_address = Column(String(100), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())