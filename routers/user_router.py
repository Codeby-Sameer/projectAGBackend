 
#user_router.py
 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.core.security import get_password_hash
from app.routers.auth_router import get_current_user  # JWT dependency
 
router = APIRouter()
 
 
# ---------------------------------------------------
# 🚫 Helper: Verify Super Admin Access
# ---------------------------------------------------
def require_super_admin(current_user: User):
    """
    Ensure only Super Admins can access certain routes.
    """
    if not current_user or current_user.role.lower() != "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Super Admins can manage users.",
        )
 
 
# ---------------------------------------------------
# 🧩 Get All Users (Super Admin only)
# ---------------------------------------------------
@router.get("/", response_model=list[UserRead])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_super_admin(current_user)
    users = db.query(User).order_by(User.id.asc()).all()
    return users
 
 
# ---------------------------------------------------
# 🧩 Get Single User by ID
# ---------------------------------------------------
@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_super_admin(current_user)
    user = db.query(User).filter(User.id == user_id).first()
 
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
 
 
# ---------------------------------------------------
# 🧩 Create New User (Super Admin only)
# ---------------------------------------------------
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_super_admin(current_user)
 
    # Prevent duplicate email
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
 
    hashed_pw = get_password_hash(user_data.password)
 
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw,
        role=user_data.role or "staff",
        is_active=user_data.is_active if user_data.is_active is not None else True,
    )
 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
 
    return new_user
 
 
# ---------------------------------------------------
# 🧩 Update User (Super Admin only)
# ---------------------------------------------------
@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_super_admin(current_user)
 
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
 
    # ✅ Check for duplicate email if updated
    if user_data.email and user_data.email != user.email:
        email_conflict = db.query(User).filter(User.email == user_data.email).first()
        if email_conflict and email_conflict.id != user.id:
            raise HTTPException(status_code=400, detail="Email already taken by another user")
        user.email = user_data.email
 
    # ✅ Apply other updates safely
    if user_data.username:
        user.username = user_data.username
    if user_data.role:
        user.role = user_data.role
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    if user_data.password:
        user.hashed_password = get_password_hash(user_data.password)
 
    db.commit()
    db.refresh(user)
    return user
 
 
# ---------------------------------------------------
# 🧩 Delete User (Super Admin only)
# ---------------------------------------------------
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_super_admin(current_user)
 
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
 
    db.delete(user)
    db.commit()
    return {"message": f"✅ User '{user.username}' deleted successfully"}
 
 
# ---------------------------------------------------
# 🧩 Toggle User Activation (Optional endpoint)
# ---------------------------------------------------
@router.patch("/{user_id}/toggle-active", status_code=status.HTTP_200_OK)
def toggle_user_active_status(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Quickly activate/deactivate user accounts.
    """
    require_super_admin(current_user)
 
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
 
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
 
    status_text = "activated" if user.is_active else "deactivated"
    return {"message": f"✅ User '{user.username}' has been {status_text}."}
 
 