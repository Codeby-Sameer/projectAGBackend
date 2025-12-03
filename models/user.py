from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from core.database import Base
 
 
class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)                     # ✅ Added for display & naming
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="recruiter")      # e.g. superadmin, recruiter, staff
    is_active = Column(Boolean, default=True)                           # ✅ To toggle user status
    created_at = Column(DateTime, default=datetime.utcnow)              # ✅ For sorting and logs
 