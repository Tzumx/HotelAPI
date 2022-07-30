from fastapi import APIRouter

router = APIRouter()


@router.get("/guests")
async def get_guests(offset: int = 0, limit: int = 100):
    """
    List guests

        Args:
                offset (int, optional): number for "offset" entries
                limit (int, optional): number for "limit" entries
        Returns:
                JSON with guests or error
    """
    pass


@router.get("/guests/filter")
async def get_guests(name: str="", email: str = "", phone: str = ""):
    """
    List guests

        Args:
            name (str, optional): Name of the guest
            email (str, optional): guest's email
            phone (str, optional): guest's phone
        Returns:
            JSON with result
    """
    pass


@router.post("/guests")
async def create_guest():
    """
    Create guest

        Args:
            name (str): Name of the guest
            email (str, optional): guest's email
            phone (str, optional): guest's phone
        Returns:
            JSON with result
    """
    pass


@router.put("/guests/{guest_id}")
async def update_guest():
    """
    Update guest

        Args:
            guest_id (int): guest's id
            name (str): Name of the guest
            email (str, optinal): guest's email
            phone (str, optinal): guest's phone
        Returns:
            JSON with result
    """
    pass


@router.delete("/guests/{guest_id}")
async def delete_guest():
    """
    Delete guest

        Args:
            guest_id (int): guest's id
        Returns:
            JSON with result
    """
    pass


@router.get("/guests/{guest_id}/bookings")
async def get_guest_bookings(is_active : bool = True):
    """
    List bookings according with guest

        Args:
            guest_id (id): Guest id
            is_active (bool, optional) : is booking active
        Returns:
            JSON with result
    """
    pass


@router.get("/guests/{guest_id}/requests")
async def get_guest_requests(is_closed: bool = False):
    """
    List requests according with guest

        Args:
            guest_id (id): Guest id
            is_closed (bool, optional): is request closed
        Returns:
            JSON with result
    """
    pass
