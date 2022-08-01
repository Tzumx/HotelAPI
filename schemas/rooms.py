from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, Field, UUID4, validator


class RoomTypeBase(BaseModel):
    """Base schema with room type details."""
    type_name: str
    price: float
    description: str


class RoomBase(BaseModel):
    """Base schema with room details."""
    number: int
    room_types_id: int
    floor: int = 0
    housing: int = 0


class FeatureBase(BaseModel):
    """Base schema for roomtype's features."""
    feature: str


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
    room_types_id: Union[int, None]

    class Config:
        orm_mode = True


class FeatureCreate(FeatureBase):
    """Create feature schema."""

    class Config:
        orm_mode = True


class FeatureInfo(FeatureBase):
    """Response schema with roomtype's features."""
    id: int

    class Config:
        orm_mode = True


class RoomDeleteInfo(BaseModel):
    """Response schema on delete action."""
    result: str


class FeatureTypeInfo(BaseModel):
    """Response schema on union data roomtype and feature."""
    feature: str


class FeatureTypeInfoFull(FeatureTypeInfo):
    """Response full schema on union data roomtype and feature."""
    type_name: str
    price: float
    description: str


class RoomFilter(BaseModel):
    """Schema for room filtering"""

    number: Optional[int]
    room_types_id: Optional[int]
    floor: Optional[int]
    housing: Optional[int]


class RoomStatus(BaseModel):
    """Schema for room status"""

    is_free: bool
    is_open_requests: bool
    is_paid: bool
