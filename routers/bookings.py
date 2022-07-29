from fastapi import APIRouter

router = APIRouter()


@router.get("/bookings")
async def get_bookings():
    """
    List bookings

        Args:
            fk_room_number (int): number of the room
            fk_guest_id (int): guest's id
            check_in (date): date of guest's move on
            check_out (date): date of guest's move out
            is_paid (bool): check if booking is paid
            is_active (bool): check if booking is active
        Returns:
            JSON with result
    """
    pass


@router.post("/bookings")
async def create_booking():
    """
    Add booking

        Args:
            fk_room_number (int): number of the room
            fk_guest_id (int): guest who is booking
            check_in (date): when move in
            check_out (date): when move out
            description (str): desription for the booking
        Returns:
            JSON with result
    """
    pass


@router.post("/bookings/{booking_id}")
async def update_bookings():
    """
    Update booking

        Args:
            booking_id (int): id of the booking
            fk_room_number (int): number of the room
            fk_guest_id (int): guest who is booking
            check_in (date): when move in
            check_out (date): when move out
            is_active (bool): if booking is active
            description (str): desription for the booking
        Returns:
            JSON with result
    """
    pass


@router.post("/bookings/{booking_id}/status")
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


@router.post("/bookings/{booking_id}/review")
async def post_booking_review():
    """
    Update client's review

        Args:
            booking_id (int): id of the booking
        Returns:
            JSON with result
    """
    pass


# @router.get("/bookings/{booking_id}/payment")
# async def get_booking_payment():
#     """
#     Update client's review

#         Args:
#             booking_id (int): id of the booking
#             is_active (bool): status of the booking
#         Returns:
#             JSON with result
#     """
#     pass
