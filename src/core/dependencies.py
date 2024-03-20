from fastapi import Security
from fastapi.security import HTTPBearer
import jwt

from core.config import settings
from auth.schema import User


def decrypt_token(token=Security(HTTPBearer())) -> User:
    try:
        token = token.credentials
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return User(**payload)
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")


def generate_token(user: dict):
    return jwt.encode(user, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
