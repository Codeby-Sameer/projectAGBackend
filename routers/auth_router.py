from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr
from core.database import get_db
from core.security import verify_password, create_access_token, get_password_hash
from models.user import User
from core.config import settings  # must have SECRET_KEY and ALGORITHM
 
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour validity
 
router = APIRouter(prefix="/auth", tags=["Authentication"])
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
 
 
# -----------------------------------
# 🔑 LOGIN ENDPOINT
# -----------------------------------
@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and issue a JWT token.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
 
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
 
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive. Contact an administrator.",
        )
 
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
 
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "email": user.email,
    }
 
 
# -----------------------------------
# 🧩 GET CURRENT USER FROM TOKEN
# -----------------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Decode JWT, validate token, and return the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or token expired.",
        headers={"WWW-Authenticate": "Bearer"},
    )
 
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
 
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
 
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated. Please contact admin.",
        )
 
    return user
 
 
# -----------------------------------
# 🧑‍💼 ADMIN-ONLY REGISTRATION
# -----------------------------------
ALLOWED_ROLES = [
    "Receptionist",
    "Manager",
    "Superadmin",
]
 
 
class RegisterUser(BaseModel):
    email: EmailStr
    password: str
    role: str
 
 
@router.post("/register")
def register_user(
    new_user: RegisterUser,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Register a new user (Administrator only).
    """
    if current_user.role.lower() != "administrator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can register new users.",
        )
 
    if new_user.role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Allowed roles: {', '.join(ALLOWED_ROLES)}"
        )
 
    existing_user = db.query(User).filter(User.email == new_user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
 
    hashed_pw = get_password_hash(new_user.password)
 
    user = User(
        email=new_user.email,
        username=new_user.email.split("@")[0],
        hashed_password=hashed_pw,
        role=new_user.role,
        is_active=True,
    )
 
    db.add(user)
    db.commit()
    db.refresh(user)
 
    return {
        "message": f"✅ User {user.email} registered successfully with role '{user.role}'",
        "email": user.email,
        "role": user.role,
    }