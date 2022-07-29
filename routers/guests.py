from fastapi import APIRouter

router = APIRouter()


@router.get("/guests")
async def get_guests():
    """
    List guests

        Args (optional):
            name (str): Name of the guest
            email (str): guest's email
            phone (str): guest's phone
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


@router.post("/guests/{guest_id}")
async def update_guest():
    """
    Update guest

        Args:
            guest_id (int): guest's id
            name (str): Name of the guest
            email (str): guest's email
            phone (str): guest's phone
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
async def get_guest_bookings():
    """
    List bookings according with guest

        Args:
            guest_id (id): Guest id
        Returns:
            JSON with result
    """
    pass


@router.get("/guests/{guest_id}/requests")
async def get_guest_requests():
    """
    List requests according with guest

        Args:
            guest_id (id): Guest id
        Returns:
            JSON with result
    """
    pass
