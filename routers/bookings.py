from fastapi import APIRouter

router = APIRouter()


@router.get("/booking")
async def bookings_get():
    """
    List bookings

        Args:
            check_in (date)
            check_out (date)
            is_paid (bool)
            is_active (bool)
        Returns:
            JSON with result
    """
    pass


@router.post("/booking")
async def booking_create():
    """
    Add booking

        Args:
            room_number (int): number of the room
            guest_id (int): guest who is booking
            check_in (date): when move in
            check_out (date): when move out
            description (str): desription for the booking
        Returns:
            JSON with result
    """
    pass


@router.post("/booking/{booking_id}")
async def bookings_update():
    """
    Update booking

        Args:
            bookig_id (int): id of the booking
            room_number (int): number of the room
            guest_id (int): guest who is booking
            check_in (date): when move in
            check_out (date): when move out
            description (str): desription for the booking
        Returns:
            JSON with result
    """
    pass


@router.post("/booking/{booking_id}/active")
async def booking_set_active(is_active: bool):
    """
    Set booking state

        Args:
            booking_id (int): id of the booking
            is_active (bool): status of the booking
        Returns:
            JSON with result
    """
    pass


@router.post("/booking/{booking_id}/review")
async def booking_post_review():
    """
    Update client's review

        Args:
            booking_id (int): id of the booking
            is_active (bool): status of the booking
        Returns:
            JSON with result
    """
    pass


@router.get("/booking/{booking_id}/payment")
async def booking_get_payment():
    """
    Update client's review

        Args:
            booking_id (int): id of the booking
            is_active (bool): status of the booking
        Returns:
            JSON with result
    """
    pass
