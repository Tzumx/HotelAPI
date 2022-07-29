from fastapi import APIRouter
from typing import List

from schemas import rooms as rooms_schema
from crud import rooms as rooms_crud

router = APIRouter()


@router.post("/roomtypes", response_model=rooms_schema.RoomTypeInfo)
async def create_room_type(roomtype: rooms_schema.RoomTypeCreate):
    """
    Create room's type
        Args:
                type_name (str): type of rooms
                price (float): price for that type
                description (str, optional): description
        Returns:
                JSON with result or error
    """
    return await rooms_crud.create_room_type(roomtype=roomtype)


@router.post("/roomtypes/{roomtype_id}", response_model=rooms_schema.RoomTypeInfo)
async def update_room_type(roomtype: rooms_schema.RoomTypeInfo):
    """
    Update info in the room's type

        Args:
                roomtype_id (int): id of the roomtype
                type_name (str): type of rooms
                price (float): price for that type
                description (str): description
        Returns:
                JSON with result or error
    """
    return await rooms_crud.update_room_type(roomtype=roomtype)


@router.delete("/roomtypes", response_model=rooms_schema.DeleteInfo)
async def delete_room_type(id: int):
    """
    Delete room's type

        Args:
                id (int): Id of entry to delete
        Returns:
                JSON with result of delete: Success or Error
    """
    return await rooms_crud.delete_room_type(id=id)


@router.get("/roomtypes", response_model=List[rooms_schema.RoomTypeInfo])
async def get_room_types(skip: int = 0, limit: int = 100):
    """
    Get list of room's types

        Args (optional):
                skip (int): number for "offset" entries
                limit (int): number for "limit" entries
        Returns:
                JSON with room's types or error
    """
    return await rooms_crud.get_room_types(skip=skip, limit=limit)


@router.post("/rooms", response_model=rooms_schema.RoomInfo)
async def create_room(room: rooms_schema.RoomCreate):
    """
    Create new room
        Args:
                number (int): room number
                fk_room_types_id (int): room's type
                floor (int,  optional): the room is located on this floor, default = 0, >=0
                housing (int,  optional): number of housing, default = 0, >=0
        Returns:
                JSON with result of creation or error
    """
    return await rooms_crud.create_room(room=room)


@router.post("/rooms/{room_id}", response_model=rooms_schema.RoomInfo)
async def update_room(room: rooms_schema.RoomInfo):
    """
    Update info in the room

        Args:
                number (int): room number
                fk_room_types_id (int): room's type
                floor (int): the room is located on this floor, default = 0
                housing (int): number of housing, default = 0
        Returns:
                JSON with result or error
    """
    return await rooms_crud.update_room(room=room)


@router.delete("/rooms", response_model=rooms_schema.DeleteInfo)
async def delete_room(number: int):
    """
    Delete room.

        Args:
                id (int): Id of entry to delete
        Returns:
                JSON with result of delete: Success or Error
    """
    return await rooms_crud.delete_room(number=number)


@router.get("/rooms", response_model=List[rooms_schema.RoomInfo])
async def get_rooms(skip: int = 0, limit: int = 100):
    """
    Get list of rooms

        Args (optional):
                skip (int): number for "offset" entries
                limit (int): number for "limit" entries
        Returns:
                JSON with rooms or error
    """
    return await rooms_crud.get_rooms(skip=skip, limit=limit)


@router.get("/rooms/{room_number}/status")  # add response model
async def room_status():  # add schema or query params
    """
    Check room's status inside a date range   

        Args:
                room_number (int): number of the room to check
                from (date,  optional): filter from date
                till (date,  optional): filter till date
        Returns:
                JSON with answer (true or false)
    """
    pass


@router.get("/rooms/{room_number}/bookings")  # add response model
async def get_room_bookings():  # add schema or query params, add filters
    """
    List bookings coresponding with that room  

        Args:
                room_number (int): number of the room to check
                from (date,  optional): filter from date
                till (date,  optional): filter till date
        Returns:
                JSON with bookings or error
    """
    pass


@router.get("/rooms/{room_number}/requests")  # add response model
async def get_room_requests():  # add schema or query params, add filters
    """
    List requests coresponding with that room  

        Args:
                room_number (int): number of the room to check
                is closed (bool): is request has closed
                from (date,  optional): filter from date
                till (date,  optional): filter till date
        Returns:
                JSON with requests or error
    """
    pass


@router.get("/rooms/{room_number}/guests")  # add response model
async def get_room_guest():  # add schema or query params
    """
    Get who in the room now

        Args:
                room_number (int): number of the room to check
        Returns:
                JSON with guest info
    """
    pass


@router.get("/rooms/{room_number}/features")  # add response model
async def get_room_features():  # add schema or query params
    """
    List features corresponding with that room

        Args:
                room_number (int): number of the room to check
        Returns:
                JSON with features
    """
    pass
