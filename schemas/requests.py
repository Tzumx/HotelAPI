from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RequestBase(BaseModel):
    """Base schema for requests"""

    description: str  # requsts's description
    price: float = 0  # price of request (if need)


class RequestCreate(RequestBase):
    """Schema for request creation"""

    booking_id: int  # id of booking that request correspond to

    class Config:
        orm_mode = True


class RequestUpdate(RequestCreate):
    """Schema for request update"""

    booking_id: Optional[int]
    description: Optional[str]
    price: Optional[float]
    is_closed: Optional[bool]  # is request closed
    close_description: Optional[str]  # requsts's description after closing

    class Config:
        orm_mode = True


class RequestInfo(RequestBase):
    """Schema for requests information"""

    id: int
    fk_booking_id: int = Field(..., alias='booking_id')
    description: Optional[str]
    is_closed: bool  # is request closed
    close_description: Optional[str]  # requsts's description after closing
    price: float
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RequestFilter(BaseModel):
    """Schema for filtering requests"""

    booking_id: Optional[int]
    is_closed: Optional[bool]
    price_from: Optional[float]
    price_till: Optional[float]
    date_creation_from: Optional[datetime]  # filter by creation date from
    date_creation_till: Optional[datetime]  # filter by creation date till


class RequestDeleteInfo(BaseModel):
    """Response schema on delete action"""

    result: str
