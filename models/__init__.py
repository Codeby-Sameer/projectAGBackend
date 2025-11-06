from sqlalchemy.orm import declarative_base
Base = declarative_base()

from .problem import Problem  # ✅ Correct class name
from .real_estate import RealEstate  # expose for imports
