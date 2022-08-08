import random
import hashlib
import string
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from crud import users as users_crud
from schemas import users as users_schema
import datetime
from typing import Union, Any
from jose import jwt
from pathlib import Path
from dotenv import load_dotenv
from os import getenv
from pydantic import ValidationError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth", scheme_name="JWT")
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

JWT_SECRET_KEY = getenv("JWT_SECRET_KEY", "secret_key")
JWT_REFRESH_SECRET_KEY = getenv(
    "JWT_REFRESH_SECRET_KEY", "seccret_refresh_key")


def get_random_string(length=12):
    """Create random string for Salt """

    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """ Hashes password with salt """

    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """ Check if password hash matches the stored hash """

    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """Short term token"""

    if expires_delta is not None:
        expires_delta = datetime.datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.datetime.utcnow() + \
            datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt, expires_delta


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """ Long term token """

    if expires_delta is not None:
        expires_delta = datetime.datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.datetime.utcnow() + \
            datetime.timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt, expires_delta


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """ Get auth user for validation """

    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = users_schema.TokenPayload(**payload)

        if datetime.datetime.fromtimestamp(token_data.exp) < datetime.datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await users_crud.get_user_by_email(payload['sub'])

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return users_schema.SystemUser(**user)
