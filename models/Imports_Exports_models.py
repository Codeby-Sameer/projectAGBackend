from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Contact(Base):
    __tablename__ = "imports_exports_contacts"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100))
    phone_number = Column(String(20))
    message = Column(Text)
