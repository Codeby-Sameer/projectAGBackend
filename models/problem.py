from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from core.database import Base
 
 
class Problem(Base):
    __tablename__ = "problems"
 
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    client_id = Column(String(100), nullable=True)
 
    business_vertical = Column(String(100), nullable=False)
    referring_source = Column(String(100), nullable=False)
    problem_category = Column(String(100), nullable=False)
    priority_level = Column(String(50), nullable=False)
 
    problem_summary = Column(Text, nullable=True)
    audio_filename = Column(String(255), nullable=True)
 
    # ✅ New fields
    status = Column(String(50), default="Pending")          # "Pending", "In Progress", "Resolved"
    is_resolved = Column(Boolean, default=False)            # quick toggle in admin
    created_at = Column(DateTime, default=datetime.utcnow)  # auto timestamp
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 