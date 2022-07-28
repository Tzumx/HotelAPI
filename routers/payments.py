from fastapi import APIRouter

router = APIRouter()


@router.get("/payment")
async def payments_get():
    """
    List payments

        Args:
            booking_id (int): id of booking that payment correspond to
            sum (float): sum of payment
            from (datetime): from the time of the payment
            till (datetime): till the time of the payment            
        Returns:
            JSON with result
    """
    pass


@router.post("/payment")
async def payment_create():
    """
    Create payment

        Args:
            booking_id (int): id of booking that payment correspond to
            sum (float): sum of payment
            date (datetime): time of the payment
            description (str): description of payment
        Returns:
            JSON with result
    """
    pass


@router.post("/payment/{payment_id}")
async def payment_update():
    """
    Create payment

        Args:
            payment_id (int): id of payment
            booking_id (int): id of booking that payment correspond to
            sum (float): sum of payment
            date (datetime): time of the payment
            description (str): description of payment
        Returns:
            JSON with result
    """
    pass
