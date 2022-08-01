from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel


class BookingBase (BaseModel):
    """Base schema with booking details."""

    room_number: Union[int, None]
    guest_id: Union[int, None]
    check_in: datetime
    check_out: datetime
    description: Optional[str]


class BookingCreate (BookingBase):
    """Schema for booking creation"""

    class Config:
        orm_mode = True


class BookingInfo (BookingBase):
    """Schema for response bookings instance"""

    id: int
    is_paid: bool
    is_active: bool
    client_review: str
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


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
