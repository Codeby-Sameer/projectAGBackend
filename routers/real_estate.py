from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from schemas.real_estate import RealEstateCreate, RealEstateRead
from services.real_estate_service import create_realestate, get_realestate, list_realestates
from core.permissions import role_required  # 🔒 RBAC import

router = APIRouter()

# 🧩 Allowed roles for Real Estate module
ALLOWED_REALESTATE_ROLES = ["Administrator", "Admin Personnel"]

# ---------------------------------------
# 🏠 CREATE Real Estate Entry
# ---------------------------------------
@router.post("/", response_model=RealEstateRead, status_code=201)
def create(
    payload: RealEstateCreate,
    db: Session = Depends(get_db),
    # role: str = Depends(role_required(ALLOWED_REALESTATE_ROLES))  # ✅ Restricted
):
    existing = get_realestate(db, payload.fileNo)
    if existing:
        raise HTTPException(status_code=400, detail="fileNo already exists")

    obj = create_realestate(db, payload)
    return obj


# ---------------------------------------
# 📋 LIST All Real Estate Records
# ---------------------------------------
@router.get("/", response_model=List[RealEstateRead])
def list_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    role: str = Depends(role_required(ALLOWED_REALESTATE_ROLES))  # ✅ Restricted
):
    return list_realestates(db, skip=skip, limit=limit)


# ---------------------------------------
# 🔍 GET Real Estate by file_no
# ---------------------------------------
@router.get("/{file_no}", response_model=RealEstateRead)
def get_one(
    file_no: str,
    db: Session = Depends(get_db),
    role: str = Depends(role_required(ALLOWED_REALESTATE_ROLES))  # ✅ Restricted
):
    obj = get_realestate(db, file_no)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj
