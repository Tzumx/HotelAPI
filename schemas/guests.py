from typing import Optional, Union
from pydantic import BaseModel


class GuestBase(BaseModel):
    """Base schema with guest details."""

    name: str


class GuestCreate(GuestBase):
    """Schema for guest creation"""

    email: Optional[str]
    phone: Optional[str]

    class Config:
        orm_mode = True


class GuestInfo (GuestBase):
    """Schema for guest information"""

    id: int
    email: str
    phone: str

    class Config:
        orm_mode = True


class GuestFilter (BaseModel):
    """Schema for guests filtering"""

    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]


class GuestDeleteInfo(BaseModel):
    """Response schema on delete action"""

    result: str
