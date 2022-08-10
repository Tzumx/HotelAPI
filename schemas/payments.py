from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PaymentBase(BaseModel):
    """Base schema for payments"""

    sum: float
    date: datetime


class PaymentCreate(PaymentBase):
    """Schema for payment create"""

    booking_id: int
    description: Optional[str] = ""

    class Config:
        orm_mode = True


class PaymentUpdate(PaymentCreate):
    """Schema for payment update"""

    booking_id: Optional[int]
    sum: Optional[float]
    date: Optional[datetime]

    class Config:
        orm_mode = True


class PaymentInfo(PaymentBase):
    """Schema for getting information about payment"""

    id: int
    fk_booking_id: int = Field(..., alias='booking_id')
    description: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PaymentFilter(BaseModel):
    """Schema for filtering payments"""

    id: Optional[int]
    booking_id: Optional[int]
    sum_from: Optional[float]
    sum_till: Optional[float]
    date_from: Optional[datetime]
    date_till: Optional[datetime]


class PaymentDeleteInfo(BaseModel):
    """Response schema on delete action"""

    result: str
