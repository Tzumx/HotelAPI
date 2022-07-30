from fastapi import APIRouter

router = APIRouter()


@router.get("/requests")
async def get_requests(offset: int = 0, limit: int = 100):
    """
    List requests

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries   
        Returns:
            JSON with result
    """
    pass


@router.post("/requests/filter")
async def filter_requests(offset: int = 0, limit: int = 100):
    """
    List requests with filter

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries           
            booking_id (int, optional): id of booking that request correspond to
            is_closed (bool, optional): is request closed
            price (float, optional): price of request
            date_from (datetime, optional): filter date from
            date_till (datetime, optional): filter date till
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
            price (float, optinal): price of request (if need)
        Returns:
            JSON with result
    """
    pass


@router.put("/requests/{request_id}")
async def update_request():
    """
    Update request

        Args:
            request_id (int): id of request
            booking_id (int): id of booking that request correspond to
            description (str): requsts's description
            is_closed (bool, optinal): is request closed
            close_description (str, optinal): requsts's description after closing
            price (float, optinal): price of request (if need)
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
