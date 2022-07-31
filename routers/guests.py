from typing import List
from fastapi import APIRouter
from schemas import guests as guests_schema, bookings as booking_schema
from schemas import requests as requests_schema

router = APIRouter()


@router.get("/guests", response_model=List[guests_schema.GuestInfo])
async def get_guests(offset: int = 0, limit: int = 100):
    """
    List guests

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries
        Returns:
            response: List[GuestInfo]
                JSON with guests
    """
    pass


@router.get("/guests/filter", response_model=List[guests_schema.GuestInfo])
async def get_guests(name: str = "", email: str = "", phone: str = ""):
    """
    List guests with filter

        Args:
            name (str, optional): Name of the guest
            email (str, optional): guest's email
            phone (str, optional): guest's phone
        Returns:
            response: List[GuestInfo]
                JSON with result
    """
    pass


@router.post("/guests", response_model=guests_schema.GuestInfo)
async def create_guest(guest: guests_schema.GuestCreate):
    """
    Create guest

        Args:
            guest: GuestCreate
                parameters required to create a guest
        Returns:
            response: GuestInfo
                JSON with resulted instance of guest
    """
    pass


@router.put("/guests/{guest_id}", response_model=guests_schema.GuestInfo)
async def update_guest(guest_id: int, guest: guests_schema.GuestCreate):
    """
    Update guest

        Args:
            guest_id (int): guest's id

            guest: GuestCreate
                parameters required to update a roomtype
        Returns:
            response: GuestInfo
                JSON with resulted instance
    """
    pass


@router.delete("/guests/{guest_id}", response_model=guests_schema.DeleteInfo)
async def delete_guest(guest_id: int):
    """
    Delete guest

        Args:
            guest_id (int): guest's id
        Returns:
            response: DeleteInfo
                JSON with result (Success, Error)
    """
    pass


@router.get("/guests/{guest_id}/bookings", response_model=List[booking_schema.BookingInfo])
async def get_guest_bookings(guest_id: int, is_active: bool = True):
    """
    List bookings connected with this guest

        Args:
            guest_id (id): guest id
            is_active (bool, optional) : is booking active
        Returns:
            response: List[BookingInfo]
                JSON with result
    """
    pass


@router.get("/guests/{guest_id}/requests", response_model=List[requests_schema.RequestInfo])
async def get_guest_requests(guest_id: int, is_closed: bool = False):
    """
    List requests connected with this guest

        Args:
            guest_id (id): guest id
            is_closed (bool, optional): is request closed
        Returns:
            response: List[RequestInfo]
                JSON with result
    """
    pass
