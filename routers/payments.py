from fastapi import APIRouter

router = APIRouter()


@router.get("/payments")
async def get_payments():
    """
    List payments

        Args:
            fk_booking_id (int): id of booking that payment correspond to
            sum (float): sum of payment
            from (datetime): filter start time of the payment
            till (datetime): filter end time of the payment            
        Returns:
            JSON with result
    """
    pass


@router.post("/payments")
async def create_payment():
    """
    Create payment

        Args:
            fk_booking_id (int): id of booking that payment correspond to
            sum (float): sum of payment
            date (datetime): time of the payment
            description (str): description of payment
        Returns:
            JSON with result
    """
    pass


@router.post("/payments/{payment_id}")
async def update_payment():
    """
    Update payment

        Args:
            payment_id (int): id of payment
            fk_booking_id (int): id of booking that payment correspond to
            sum (float): sum of payment
            date (datetime): time of the payment
            description (str): description of payment
        Returns:
            JSON with result
    """
    pass


@router.delete("/payments/{payment_id}")
async def delete_payment():
    """
    Delete payment

        Args:
            payment_id (int): id of payment

        Returns:
            JSON with result
    """
    pass
