from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field


class BookingBase (BaseModel):
    """Base schema with booking details."""

    room_number: Union[int, None]
    guest_id: Union[int, None]
    check_in: datetime
    check_out: datetime
    description: Optional[str]


class BookingCreate (BookingBase):
    """Schema for booking creation"""

    room_number: int
    guest_id: int

    class Config:
        orm_mode = True


class BookingUpdate(BookingCreate):
    """Schema for booking update"""

    room_number: Optional[int]
    guest_id: Optional[int]
    is_active: Optional[bool]
    client_review: Optional[str]
    check_in: Optional[datetime]
    check_out: Optional[datetime]

    class Config:
        orm_mode = True


class BookingInfo (BaseModel):
    """Schema for response bookings instance"""

    id: int
    fk_room_number: Union[int, None] = Field(..., alias='room_number')
    fk_guest_id: Union[int, None] = Field(..., alias='guest_id')
    check_in: datetime
    check_out: datetime
    description: Optional[str]
    is_paid: Optional[bool]
    is_active: Optional[bool]
    client_review: Optional[str]
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class BookingFilter (BaseModel):
    """Filter bookings"""

    room_number: Optional[int]
    guest_id: Optional[int]
    is_paid: Optional[bool]
    is_active: Optional[bool]
    check_in_from: Optional[datetime]
    check_in_till: Optional[datetime]
    check_out_from: Optional[datetime]
    check_out_till: Optional[datetime]


class BookingDeleteInfo (BaseModel):
    """Response schema on delete action"""

    result: str


class BookingSumInfo (BaseModel):
    """Response schema with full information about amount of money for booking"""

    sum: float


class BookingReview (BaseModel):
    """Schema for client review"""

    review: str
