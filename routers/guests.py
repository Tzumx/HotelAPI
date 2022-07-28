from fastapi import APIRouter

router = APIRouter()


@router.get("/guest")
async def guests_get():
    """
    List guests

        Args:
            name (str): Name of the guest
            email (str): guest's email
            phone (str): guest's phone
        Returns:
            JSON with result
    """
    pass


@router.post("/guest")
async def guest_create():
    """
    Create guest

        Args:
            name (str): Name of the guest
            email (str): guest's email
            phone (str): guest's phone
        Returns:
            JSON with result
    """
    pass


@router.post("/guest/{guest_id}")
async def guest_update():
    """
    Create guest

        Args:
            name (str): Name of the guest
            email (str): guest's email
            phone (str): guest's phone
        Returns:
            JSON with result
    """
    pass


@router.get("/guest/{guest_id}/booking")
async def guest_get_bookings():
    """
    List bookings according with guest

        Args:
            guest_id (id): Guest id
        Returns:
            JSON with result
    """
    pass


@router.get("/guest/{guest_id}/request")
async def guest_get_requests():
    """
    List requests according with guest

        Args:
            guest_id (id): Guest id
        Returns:
            JSON with result
    """
    pass
