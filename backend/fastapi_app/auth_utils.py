import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import jwt
from passlib.hash import django_pbkdf2_sha256
from jose import JWTError, jwt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))


def hash_password(password: str) -> str:
    return django_pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return django_pbkdf2_sha256.verify(password, hashed_password)


def create_access_token(user_id: int, email: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=JWT_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str):
    try:
        return jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
    except JWTError:
        return None