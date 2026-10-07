from datetime import datetime
from uuid import uuid4

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_app.auth_utils import (
    create_access_token,
    hash_password,
    verify_password,
)
from fastapi_app.database import get_db
from fastapi_app.models import User, UserProfile
from fastapi_app.schemas import TokenResponse, UserLogin, UserRegister


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


bearer_scheme = HTTPBearer()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
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


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = db.scalar(
        select(User).where(User.email == user_data.email)
    )

    if not user or not verify_password(
        user_data.password,
        user.password,
    ):
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


def _get_auth0_config():
    import os

    domain = os.getenv("AUTH0_DOMAIN")
    audience = os.getenv("AUTH0_AUDIENCE")

    if not domain or not audience:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Auth0 is not configured",
        )

    domain = domain.replace("https://", "").rstrip("/")

    return domain, audience


def _get_auth0_user(token: str):
    domain, audience = _get_auth0_config()

    try:
        with httpx.Client(timeout=10.0) as client:
            jwks_response = client.get(
                f"https://{domain}/.well-known/jwks.json"
            )
            jwks_response.raise_for_status()
            jwks = jwks_response.json()

        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        key = next(
            (
                item
                for item in jwks.get("keys", [])
                if item.get("kid") == kid
            ),
            None,
        )

        if not key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Auth0 signing key not found",
            )

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=audience,
            issuer=f"https://{domain}/",
        )

        return payload

    except HTTPException:
        raise

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Auth0 token",
        )

    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to contact Auth0",
        )


@router.post(
    "/auth0",
    response_model=TokenResponse,
)
def auth0_login(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
):
    auth0_token = credentials.credentials

    payload = _get_auth0_user(auth0_token)

    email = payload.get("email")
    name = (
        payload.get("name")
        or payload.get("nickname")
        or ""
    )

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Auth0 token does not contain an email",
        )

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if not user:
        user = User(
            username=email,
            first_name=name,
            last_name="",
            email=email,
            password=hash_password(
                f"auth0_{uuid4().hex}"
            ),
            is_superuser=False,
            is_staff=False,
            is_active=True,
            date_joined=datetime.now(),
        )

        db.add(user)
        db.flush()

        profile = UserProfile(
            user_id=user.id,
            role="customer",
            phone=None,
        )

        db.add(profile)

    else:
        if name:
            user.first_name = name

    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        role="customer",
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }