from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator


class UserCreate(BaseModel):
    """ Check sign-up request """

    email: EmailStr
    name: str
    password: str


class UserOut(BaseModel):
    """ User answer """

    id: int
    email: str
    name: str
    # token: dict


class SystemUser(UserOut):
    """ Auth User check """

    hashed_password: str


class UserBase(BaseModel):
    """ User information answer """

    id: int
    email: EmailStr
    name: str


class TokenBase(BaseModel):
    """ Token check """

    token: UUID = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(self, value):
        """ Convert UUID """

        return value.hex


class User(UserBase):
    """ User information """

    token: TokenBase = {}
    is_active: bool


class TokenSchema(BaseModel):
    """ Token schema """

    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    """ Token check auth """

    sub: str = None
    exp: int = None
