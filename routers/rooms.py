from fastapi import APIRouter
from typing import List

from schemas import rooms as rooms_schema
from crud import rooms as rooms_crud

router = APIRouter()


@router.post("/roomtypes", response_model=rooms_schema.RoomTypeInfo)
async def create_room_types(roomtype: rooms_schema.RoomTypeCreate):
    """
    Create room's type

        Args:
                type (str): type of rooms
                number_of_rooms (int): room size
                price (float): price for that type
                description (str): description
        Returns:
                Dict with result
    """
    return await rooms_crud.create_room_types(roomtype=roomtype)


@router.delete("/roomtypes", response_model=rooms_schema.DeleteInfo)
async def delete_room_types(id: int):
    """
    Delete room's type

        Args:
                id (int): Id of entry to delete
        Returns:
                Dict with result of creation or error
    """
    return await rooms_crud.delete_room_types(id=id)


@router.get("/roomtypes", response_model=List[rooms_schema.RoomTypeInfo])
async def get_room_types(skip: int = 0, limit: int = 100):
    """
    Get list of room's types

        Args:
                skip (int): number for "offset" entries
                limit (int): number for "limit" entries
        Returns:
                List of dicts with room's types
    """
    return await rooms_crud.get_room_types(skip=skip, limit=limit)


@router.post("/rooms", response_model=rooms_schema.RoomInfo)
async def create_rooms(room: rooms_schema.RoomCreate):
    """
    Add new room

        Args:
                number (int): room number
                type_id (int): room's type
                is_free (bool): is room free
                is_clean (bool): is room clean
                is_broken (bool): is something broken in the room
        Returns:
                Dict with result of creation or error
    """
    return await rooms_crud.create_rooms(room=room)


@router.delete("/rooms", response_model=rooms_schema.DeleteInfo)
async def delete_rooms(id: int):
    """
    Delete room.

        Args:
                id (int): Id of entry to delete
        Returns:
                Dict with result
    """
    return await rooms_crud.delete_rooms(id=id)


@router.get("/rooms", response_model=List[rooms_schema.RoomInfo])
async def get_rooms(skip: int = 0, limit: int = 100):
    """
    Get list of rooms
    
        Args:
                skip (int): number for "offset" entries
                limit (int): number for "limit" entries
        Returns:
                List of dicts with rooms
    """
    return await rooms_crud.get_rooms(skip=skip, limit=limit)
