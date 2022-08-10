from fastapi import APIRouter, Depends
from schemas import bookings as bookings_schema, users as users_schema
from crud import bookings as bookings_crud
from typing import List
from utils import users as users_utils

router = APIRouter()


@router.post("/bookings/filter", response_model=List[bookings_schema.BookingInfo])
async def filter_bookings(filter: bookings_schema.BookingFilter,
                          offset: int = 0, limit: int = 100):
    """
    Add booking

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries

            booking: BookingFilter
                parameters for filtering, optional
        Returns:
            response: List[BookingInfo]
                JSON with results
    """
    return await bookings_crud.filter_bookings(filter=filter, offset=offset, limit=limit)


@router.post("/bookings", response_model=bookings_schema.BookingInfo)
async def create_booking(booking: bookings_schema.BookingCreate,
                         user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Add booking

        Args:
            booking: BookingCreate
                parameters required to create a booking
        Returns:
            response: BookingInfo
                JSON with booking instance
    """
    return await bookings_crud.create_booking(booking=booking)


@router.put("/bookings/{booking_id}", response_model=bookings_schema.BookingUpdate)
async def update_bookings(booking_id: int,
                          booking: bookings_schema.BookingUpdate,
                          user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Update specific booking.
        Args:
            booking: BookingInfo
                parameters required to update a booking
        Raises:
        Returns:
            response: BookingInfo
                JSON with updated booking instance
    """
    return await bookings_crud.update_booking(booking_id=booking_id, booking=booking)


@router.delete("/bookings/{booking_id}", response_model=bookings_schema.BookingDeleteInfo)
async def delete_bookings(booking_id: int,
                          user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Delete booking

        Args:
            booking_id (int): id of the booking
        Returns:
            response: DeleteInfo
                JSON with result (Success, Error)
    """
    return await bookings_crud.delete_booking(booking_id=booking_id)


@router.patch("/bookings/{booking_id}/is_active", response_model=bookings_schema.BookingInfo)
async def set_booking_status(booking_id: int, is_active: bool,
                             user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Set booking state

        Args:
            booking_id (int): id of the booking
            is_active (bool): status of the booking
        Returns:
            response: BookingInfo
                JSON with updated booking instance
    """
    return await bookings_crud.set_booking_status(booking_id=booking_id, is_active=is_active)


@router.patch("/bookings/{booking_id}/review", response_model=bookings_schema.BookingInfo)
async def post_booking_review(booking_id: int, review: str,
                              user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Update client's review

        Args:
            booking_id (int): id of the booking
            review (str): client's review
        Returns:
            response: BookingInfo
                JSON with updated booking instance
    """
    return await bookings_crud.post_booking_review(booking_id=booking_id, review=review)

@router.get("/bookings/{booking_id}/sum")
async def get_booking_sum(booking_id: int):
    """
    Get amount of services for the booking

        Args:
            booking_id (int): id of the booking
        Returns:
            response: List[BookingSum]
                JSON with amount
    """
    return await bookings_crud.get_booking_sum(booking_id=booking_id)