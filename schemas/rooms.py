from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, UUID4, validator


class RoomTypeBase(BaseModel):
    """Base schema with room type details."""
    type: str
    price: float
    description: str
    is_doublebad: bool = False
    is_kitchen: bool = False
    is_bathroom: bool = False
    is_conditioner: bool = False
    is_TV: bool = False


class RoomBase(BaseModel):
    """Base schema with room details."""
    number: int
    type_id: int
    is_clean: bool = True


class RoomTypeCreate(RoomTypeBase):
    """Create type of rooms schema."""

    class Config:
        orm_mode = True


class RoomTypeInfo(RoomTypeBase):
    """Response schema with room type details."""
    id: int

    class Config:
        orm_mode = True


class RoomCreate(RoomBase):
    """Create rooms schema."""

    class Config:
        orm_mode = True


class RoomInfo(RoomBase):
    """Response schema with room details."""
    id: int

    class Config:
        orm_mode = True

class DeleteInfo(BaseModel):
    """Response schema on delete action"""
    result: str