from typing import Optional

from pydantic import BaseModel, EmailStr


class GuestBase(BaseModel):
    """Base schema with guest details."""

    name: str


class GuestCreate(GuestBase):
    """Schema for guest creation"""

    email: Optional[EmailStr]
    phone: Optional[str]

    class Config:
        orm_mode = True


class GuestUpdate(GuestCreate):
    """Schema for guest update"""

    name: Optional[str]

    class Config:
        orm_mode = True


class GuestInfo (GuestBase):
    """Schema for guest information"""

    id: int
    email: Optional[EmailStr]
    phone: Optional[str]

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
