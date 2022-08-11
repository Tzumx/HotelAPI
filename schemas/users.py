from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator


class UserCreate(BaseModel):
    """ Check sign-up request """

    email: EmailStr
    name: str
    password: str


class UserBase(BaseModel):
    """ User information answer """

    id: int
    email: EmailStr
    name: str


class UserInfo(UserBase):
    """ User full answer """

    is_active: Optional[bool]
    is_admin: Optional[bool]


class SystemUser(UserInfo):
    """ Auth User check """

    hashed_password: str


class TokenBase(BaseModel):
    """ Token check """

    token: UUID = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(cls, value):
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


class TokenRefreshSchema(BaseModel):
    """ Token refesh schema """

    access_token: str


class TokenPayload(BaseModel):
    """ Token check auth """

    sub: str = None
    exp: int = None


class UserFilter(BaseModel):
    """ User filter """

    id: Optional[int]
    email: Optional[str]
    name: Optional[str]


class UserUpdate(BaseModel):
    """ User filter """

    email: Optional[EmailStr]
    name: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
    is_admin: Optional[bool]


class UserDeleteInfo(BaseModel):

    """Response schema on delete action."""
    result: str
