from fastapi import APIRouter

router = APIRouter()


@router.get("/request")
async def requests_gets():
    """
    List requests

        Args:
            booking_id (int): id of booking that request correspond to
            is_closed (bool): is request closed
            price (float): price of request
        Returns:
            JSON with result
    """
    pass


@router.post("/request")
async def request_create():
    """
    Create request

        Args:
            booking_id (int): id of booking that request correspond to
            description (str): requsts's description
            is_closed (bool): is request closed
            close_description (str): requsts's description after closing
            price (float): price of request (if need)
        Returns:
            JSON with result
    """
    pass
