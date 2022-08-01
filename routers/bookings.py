from fastapi import APIRouter
from schemas import bookings as booking_schema
from typing import List

router = APIRouter()


@router.get("/bookings", response_model=List[booking_schema.BookingInfo])
async def get_bookings(offset: int = 0, limit: int = 100):
    """
    List bookings

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries
        Returns:
            response: List[BookingInfo]
                JSON with results
    """
    pass


@router.post("/bookings/filter", response_model=List[booking_schema.BookingInfo])
async def filter_bookings(filter: booking_schema.BookingFilter,
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
    pass


@router.post("/bookings", response_model=booking_schema.BookingInfo)
async def create_booking(booking: booking_schema.BookingCreate):
    """
    Add booking

        Args:
            booking: BookingCreate
                parameters required to create a booking
        Returns:
            response: BookingInfo
                JSON with booking instance
    """
    pass


@router.put("/bookings/{booking_id}", response_model=booking_schema.BookingInfo)
async def update_bookings(booking_id: int,
                          booking: booking_schema.BookingInfo):
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
    pass


@router.delete("/bookings/{booking_id}", response_model=booking_schema.BookingDeleteInfo)
async def delete_bookings(booking_id: int):
    """
    Delete booking

        Args:
            booking_id (int): id of the booking
        Returns:
            response: DeleteInfo
                JSON with result (Success, Error)
    """
    pass


@router.patch("/bookings/{booking_id}/is_active", response_model=booking_schema.BookingInfo)
async def set_booking_status(booking_id: int, is_active: bool):
    """
    Set booking state

        Args:
            booking_id (int): id of the booking
            is_active (bool): status of the booking
        Returns:
            response: BookingInfo
                JSON with updated booking instance
    """
    pass


@router.patch("/bookings/{booking_id}/review", response_model=booking_schema.BookingInfo)
async def post_booking_review(booking_id: int, review: str):
    """
    Update client's review

        Args:
            booking_id (int): id of the booking
            review (str): client's review
        Returns:
            response: BookingInfo
                JSON with updated booking instance
    """
    pass
