from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_app.auth_utils import hash_password, verify_password, create_access_token
from fastapi_app.database import get_db
from fastapi_app.models import User, UserProfile
from fastapi_app.schemas import TokenResponse, UserLogin, UserRegister

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    existing_user = db.scalar(
        select(User).where(User.email == user_data.email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    existing_username = db.scalar(
        select(User).where(User.username == user_data.email)
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already in use",
        )

    new_user = User(
        username=user_data.email,
        first_name=user_data.name,
        last_name="",
        email=user_data.email,
        password=hash_password(user_data.password),
        is_superuser=False,
        is_staff=False,
        is_active=True,
        date_joined=datetime.now(),
    )

    db.add(new_user)
    db.flush()

    new_profile = UserProfile(
        user_id=new_user.id,
        role="customer",
        phone=user_data.phone,
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "email": new_user.email,
        "role": "customer",
    }


@router.post("/login", response_model=TokenResponse)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = db.scalar(
        select(User).where(User.email == user_data.email)
    )

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    role = "customer"

    if user.is_superuser:
        role = "admin"
    elif user.is_staff:
        role = "staff"
    elif user.profile:
        role = user.profile.role

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        role=role,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }