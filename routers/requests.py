from fastapi import APIRouter

router = APIRouter()


@router.get("/requests")
async def get_requests():
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


@router.post("/requests")
async def create_request():
    """
    Create request

        Args:
            booking_id (int): id of booking that request correspond to
            description (str): requsts's description
            close_description (str): requsts's description after closing
            price (Optional[float]): price of request (if need)
        Returns:
            JSON with result
    """
    pass

@router.post("/requests/{request_id}")
async def create_request():
    """
    Update request

        Args:
            request_id (int): id of request
            booking_id (int): id of booking that request correspond to
            description (str): requsts's description
            close_description (str): requsts's description after closing
            price (Optional[float]): price of request (if need)
        Returns:
            JSON with result
    """
    pass

@router.delete("/requests/{request_id}")
async def delete_request():
    """
    Delete request

        Args:
            request_id (int): id of request
        Returns:
            JSON with result
    """
    pass