from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, UUID4, validator

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


class TokenBase(BaseModel):
    """ Token check """

    token: UUID4 = Field(..., alias="access_token")
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
