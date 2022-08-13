from typing import List

from fastapi import APIRouter, Depends

from crud import guests as guests_crud
from schemas import guests as guests_schema
from schemas import requests as requests_schema
from schemas import users as users_schema
from utils import users as users_utils

router = APIRouter()


@router.post("/guests/filter", response_model=List[guests_schema.GuestInfo],
                               tags=["guests"])
async def filter_guests(filter: guests_schema.GuestFilter = guests_schema.GuestFilter(**{}),
                        offset: int = 0, limit: int = 100,
                        user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    List guests with filter

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries

            room: GuestFilter
                parameters required to filter guests
        Returns:
            response: List[GuestInfo]
                JSON with result
    """
    return await guests_crud.filter_guests(filter=filter, offset=offset, limit=limit)


@router.post("/guests", response_model=guests_schema.GuestInfo,
                        tags=["guests"])
async def create_guest(guest: guests_schema.GuestCreate,
                       user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Create guest

        Args:
            guest: GuestCreate
                parameters required to create a guest
        Returns:
            response: GuestInfo
                JSON with resulted instance of guest
    """
    return await guests_crud.create_guest(guest=guest)


@router.put("/guests/{guest_id}", response_model=guests_schema.GuestInfo,
                                  tags=["guests"])
async def update_guest(guest_id: int, guest: guests_schema.GuestUpdate,
                       user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Update guest

        Args:
            guest_id (int): guest's id

            guest: GuestCreate
                parameters required to update a roomtype
        Returns:
            response: GuestInfo
                JSON with resulted instance
    """
    return await guests_crud.update_guest(guest_id=guest_id, guest=guest)


@router.delete("/guests/{guest_id}", response_model=guests_schema.GuestDeleteInfo,
                                     tags=["guests"])
async def delete_guest(guest_id: int,
                       user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Delete guest

        Args:
            guest_id (int): guest's id
        Returns:
            response: DeleteInfo
                JSON with result (Success, Error)
    """
    return await guests_crud.delete_guest(guest_id=guest_id)


@router.get("/guests/{guest_id}/requests", response_model=List[requests_schema.RequestInfo],
                                           tags=["guests"])
async def get_guest_requests(guest_id: int, is_closed: bool = False,
                             user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    List requests connected with this guest

        Args:
            guest_id (id): guest id
            is_closed (bool, optional): is request closed
        Returns:
            response: List[RequestInfo]
                JSON with result
    """
    return await guests_crud.get_guest_requests(guest_id=guest_id, is_closed=is_closed)
