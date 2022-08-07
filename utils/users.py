import random
import hashlib
import string
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from crud import users as users_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


def get_random_string(length=12):
    """Create random string for Salt """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """ Hashes password with salt """
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """ Check if password hash matches the stored hash """
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed

