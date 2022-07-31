from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel


class RequestBase(BaseModel):
    """Base schema for requests"""

    booking_id: int  # id of booking that request correspond to
    description: str  # requsts's description
    price: float = 0  # price of request (if need)


class RequestCreate(RequestBase):
    """Schema for request creation"""

    class Config:
        orm_mode = True


class RequestInfo(RequestBase):
    """Schema for requests information"""

    id: int
    is_closed: bool  # is request closed
    close_description: str  # requsts's description after closing
    price: float
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class RequestFilter(BaseModel):
    """Schema for filtering requests"""

    booking_id: Optional[int]
    is_closed: Optional[bool]
    price: Optional[float]
    date_creation_from: Optional[datetime]  # filter by creation date from
    date_creation_till:  Optional[datetime]  # filter by creation date till


class DeleteInfo(BaseModel):
    """Response schema on delete action"""

    result: str
