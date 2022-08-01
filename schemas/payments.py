from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel


class PaymentBase(BaseModel):
    """Base schema for payments"""

    booking_id: int
    sum: float
    date: datetime


class PaymentCreate(PaymentBase):
    """Schema for payment create"""

    description: Optional[str]

    class Config:
        orm_mode = True


class PaymentInfo(PaymentBase):
    """Schema for getting information about payment"""

    id: int
    description: str

    class Config:
        orm_mode = True


class PaymentFilter(BaseModel):
    """Schema for filtering payments"""

    id: Optional[int]
    booking_id: Optional[int]
    date_from: Optional[datetime]
    date_till: Optional[datetime]


class PaymentDeleteInfo(BaseModel):
    """Response schema on delete action"""

    result: str
