from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.company import Company
from app.models.permission import RolePermission
from app.schemas.auth import (
    LoginRequest, RegisterRequest, RefreshRequest, AuthUserResponse,
)
from app.schemas.user import OnboardingData
from app.services.auth import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    decode_token, get_current_user,
)
from app.services.permissions import normalize_role, permission_keys_for_role

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def _user_data(user: User, db: Session) -> dict:
    role_key = normalize_role(user.role)
    overrides = {
        row.permission_key: row.allowed
        for row in db.query(RolePermission).filter(RolePermission.role_key == role_key).all()
    }
    user_data = AuthUserResponse.model_validate(user).model_dump()
    user_data["role_key"] = role_key
    user_data["permissions"] = permission_keys_for_role(role_key, overrides)
    return user_data


def _token_response(user: User, db: Session) -> dict:
    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    refresh_token = create_refresh_token({"sub": str(user.id), "email": user.email})
    return {
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": _user_data(user, db),
        }
    }


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=data.name,
        email=data.email,
        phone=data.phone,
        role=data.role,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _token_response(user, db)


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return _token_response(user, db)


@router.post("/refresh")
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(data.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"data": {"access_token": access_token, "token_type": "bearer"}}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"data": _user_data(current_user, db)}


@router.get("/status")
def get_status(db: Session = Depends(get_db)):
    onboarded_user = db.query(User).filter(User.is_primary == True).first()
    return {"data": {"onboarded": onboarded_user is not None}}


@router.post("/onboarding")
def complete_onboarding(
    data: OnboardingData,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.company_id is not None:
        raise HTTPException(status_code=400, detail="User already belongs to a company")

    company = Company(**data.company)
    db.add(company)
    db.flush()

    current_user.company_id = company.id
    current_user.is_primary = True
    current_user.device_id = data.device_id or current_user.device_id
    current_user.location_lat = data.location_lat
    current_user.location_lng = data.location_lng
    current_user.user_agent = data.user_agent or request.headers.get("user-agent", "")
    current_user.ip_address = request.client.host if request.client else ""
    current_user.terms_accepted = data.terms_accepted
    db.commit()
    db.refresh(current_user)

    user_data = _user_data(current_user, db)
    return {"data": {"user": user_data, "onboarded": True}}
