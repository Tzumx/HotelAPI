from fastapi import APIRouter
from typing import List

from schemas import rooms as rooms_schema
from crud import rooms as rooms_utils

router = APIRouter()


@router.post("/roomtype", response_model=rooms_schema.RoomTypeInfo)
async def rooms_type_create(roomtype: rooms_schema.RoomTypeCreate):
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
    return await rooms_utils.create_room_type(roomtype=roomtype)


@router.post("/roomtype/{roomtype_id}", response_model=rooms_schema.RoomTypeInfo)
async def rooms_type_update(roomtype: rooms_schema.RoomTypeInfo):
    """
    Update info in the room's type

        Args:
                roomtype_id (int): id of the roomtype
                type (str): type of rooms
                number_of_rooms (int): room size
                price (float): price for that type
                description (str): description
        Returns:
                JSON with result
    """
    return await rooms_utils.create_room_type(roomtype=roomtype)


@router.delete("/roomtype", response_model=rooms_schema.DeleteInfo)
async def rooms_type_delete(id: int):
    """
    Delete room's type

        Args:
                id (int): Id of entry to delete
        Returns:
                Dict with result of creation or error
    """
    return await rooms_utils.delete_room_type(id=id)


@router.get("/roomtype", response_model=List[rooms_schema.RoomTypeInfo])
async def rooms_types_get(skip: int = 0, limit: int = 100):
    """
    Get list of room's types

        Args:
                skip (int): number for "offset" entries
                limit (int): number for "limit" entries
        Returns:
                List of dicts with room's types
    """
    return await rooms_utils.get_rooms_types(skip=skip, limit=limit)


@router.post("/room", response_model=rooms_schema.RoomInfo)
async def room_create(room: rooms_schema.RoomCreate):
    """
    Add new room

        Args:
                number (int): room number
                type_id (int): room's type
                is_free (bool): is room free
                is_broken (bool): is something broken in the room
        Returns:
                Dict with result of creation or error
    """
    return await rooms_utils.create_room(room=room)


@router.post("/room/{room_id}", response_model=rooms_schema.RoomInfo)
async def room_update(room: rooms_schema.RoomInfo):
    """
    Update info in the room

        Args:
                room_id (int): room's id
                number (int): room number
                type_id (int): room's type
                is_free (bool): is room free
                is_broken (bool): is something broken in the room
        Returns:
                JSON with result
    """
    return await rooms_utils.create_room(room=room)


@router.delete("/room", response_model=rooms_schema.DeleteInfo)
async def room_delete(id: int):
    """
    Delete room.

        Args:
                id (int): Id of entry to delete
        Returns:
                Dict with result
    """
    return await rooms_utils.delete_room(id=id)


@router.get("/room", response_model=List[rooms_schema.RoomInfo])
async def rooms_get(skip: int = 0, limit: int = 100):
    """
    Get list of rooms

        Args:
                skip (int): number for "offset" entries
                limit (int): number for "limit" entries
        Returns:
                List of dicts with rooms
    """
    return await rooms_utils.get_rooms(skip=skip, limit=limit)


@router.get("/room/{room_number}/free")  # add response model
async def room_is_free():  # add schema or query params
    """
        Check whether room is free or not inside a date range   
        Args:
                room_number (int): number of the room to check
                from (date): from which date
                till (date): till which date
        Returns:
                JSON with answer (true or false)
    """
    pass


@router.get("/room/{room_number}/booking")  # add response model
async def room_get_bookings():  # add schema or query params, add filters
    """
        List bookings coresponding with that room  
        Args:
                room_number (int): number of the room to check
        Returns:
                JSON with bookings
    """
    pass


@router.get("/room/{room_number}/request")  # add response model
async def room_get_requests():  # add schema or query params, add filters
    """
        List requests coresponding with that room  
        Args:
                room_number (int): number of the room to check
                is closed (bool): is request has closed
        Returns:
                JSON with requests
    """
    pass


@router.get("/room/{room_number}/guest")  # add response model
async def room_get_guest():  # add schema or query params
    """
        Get who in the room now
        Args:
                room_number (int): number of the room to check
        Returns:
                JSON with guest info
    """
    pass


@router.get("/room/{room_number}/feature")  # add response model
async def room_get_features():  # add schema or query params
    """
        List features corresponding with that room
        Args:
                room_number (int): number of the room to check
        Returns:
                JSON with features
    """
    pass
