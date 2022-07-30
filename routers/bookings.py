from fastapi import APIRouter

router = APIRouter()


# TODO: add schemas

@router.get("/bookings")
async def get_bookings(offset: int = 0, limit: int = 100):
    """
    List bookings

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries
        Returns:
            JSON with result
    """
    pass


@router.post("/bookings/filter")
async def filter_bookings(offset: int = 0, limit: int = 100):
    """
    Add booking

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries
            booking: BookingFilter
        Returns:
            response: List[BookingInfo]
                JSON with result
    """
    pass


@router.post("/bookings")
async def create_booking():
    """
    Add booking

        Args:
            room_number (int): number of the room
            guest_id (int): guest who is booking
            check_in (date): when move in
            check_out (date): when move out
            description (str, optional): desription for the booking
        Returns:
            JSON with result
    """
    pass


@router.put("/bookings/{booking_id}")
async def update_bookings():
    """
    Update specific booking.
        Args:
            request: UpdateBookingRequest
                parameters required to update a booking
        Raises:
        Returns:
            response: UpdateBookingResponse
    """
    pass


@router.delete("/bookings/{booking_id}")
async def delete_bookings():
    """
    Delete booking

        Args:
            booking_id (int): id of the booking
        Returns:
            JSON with result
    """
    pass


@router.patch("/bookings/{booking_id}/status")
async def set_booking_status(status: bool):
    """
    Set booking state

        Args:
            booking_id (int): id of the booking
            is_active (bool): status of the booking
        Returns:
            JSON with result
    """
    pass


@router.patch("/bookings/{booking_id}/review")
async def post_booking_review():
    """
    Update client's review

        Args:
            booking_id (int): id of the booking
        Returns:
            JSON with result
    """
    pass


# @router.get("/bookings/{booking_id}/payments")
# async def get_booking_payments():
#     """
#     Get client's payments

#         Args:
#             booking_id (int): id of the booking
#         Returns:
#             JSON with result
#     """
#     pass
