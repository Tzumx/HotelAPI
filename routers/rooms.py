from datetime import datetime
from fastapi import APIRouter
from typing import List, Optional

from schemas import rooms as rooms_schema, bookings as bookings_schema
from schemas import guests as guests_schema, requests as requests_schema
from crud import rooms as rooms_crud

router = APIRouter()


@router.get("/roomtypes", response_model=List[rooms_schema.RoomTypeInfo])
async def get_room_types(offset: int = 0, limit: int = 100):
    """
    Get list of room's types

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries
        Returns:
            response: List[RoomTypeInfo]
                JSON with room's types
    """
    return await rooms_crud.get_room_types(offset=offset, limit=limit)


@router.post("/roomtypes", response_model=rooms_schema.RoomTypeInfo)
async def create_room_type(roomtype: rooms_schema.RoomTypeCreate):
    """
    Create room's type

        Args:
            roomtype: RoomTypeCreate
                parameters required to create a roomtype
        Returns:
            response: RoomTypeInfo
                instance of created roomtype
    """
    return await rooms_crud.create_room_type(roomtype=roomtype)


@router.put("/roomtypes/{roomtype_id}", response_model=rooms_schema.RoomTypeInfo)
async def update_room_type(roomtype_id: int, roomtype: rooms_schema.RoomTypeInfo):
    """
    Update info in the room's type

        Args:
            roomtype: RoomTypeInfo
                parameters required to update a roomtype
        Returns:
            response: RoomTypeInfo
                instance of updated roomtype
    """
    return await rooms_crud.update_room_type(roomtype=roomtype)


@router.delete("/roomtypes/{roomtype_id}", response_model=rooms_schema.DeleteInfo)
async def delete_room_type(roomtype_id: int):
    """
    Delete room's type

        Args:
            id (int): Id of entry to delete
        Returns:
            response: DeleteInfo
                JSON with result of delete: Success or Error
    """
    return await rooms_crud.delete_room_type(id=roomtype_id)


@router.get("/rooms", response_model=List[rooms_schema.RoomInfo])
async def get_rooms(offset: int = 0, limit: int = 100):
    """
    Get list of rooms

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries
        Returns:
            response: List[RoomInfo]
                JSON with rooms or error
    """
    return await rooms_crud.get_rooms(offset=offset, limit=limit)


@router.post("/rooms/filter", response_model=List[rooms_schema.RoomInfo])
async def filter_rooms(room: rooms_schema.RoomFilter,
                       offset: int = 0, limit: int = 100):
    """
    Get list of rooms with filter

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries

            room: RoomInfo
                parameters required to filter rooms
        Returns:
            response: List[RoomInfo]
                JSON with rooms or error
    """
    pass


@router.post("/rooms", response_model=rooms_schema.RoomInfo)
async def create_room(room: rooms_schema.RoomCreate):
    """
    Create new room
        Args:
            room: RoomCreate
                parameters required to create a room
        Returns:
            response: RoomInfo
                JSON with created room instance
    """
    return await rooms_crud.create_room(room=room)


@router.put("/rooms/{number}", response_model=rooms_schema.RoomInfo)
async def update_room(number:int, room: rooms_schema.RoomInfo):
    """
    Update info in the room

        Args:
            number (int): room number
            room: RoomInfo
                parameters required to update a room
        Returns:
            response: RoomInfo
                JSON with updated room instance
    """
    return await rooms_crud.update_room(room=room)


@router.delete("/rooms/{number}", response_model=rooms_schema.DeleteInfo)
async def delete_room(number: int):
    """
    Delete room.

        Args:
                number (int): Id of entry to delete
        Returns:
                response: DeleteInfo
                    JSON with result of delete: Success or Error
    """
    return await rooms_crud.delete_room(number=number)


@router.get("/rooms/{number}/status", response_model=rooms_schema.RoomStatus)
async def room_status(number:int):
    """
    Check room's status   

        Args:
            number (int): number of the room to check
        Returns:
            response: RoomStatus
                JSON with status
    """
    pass


@router.get("/rooms/{number}/bookings", response_model=List[bookings_schema.BookingInfo])
async def get_room_bookings(number: int, 
                            date_from: Optional[datetime], date_till: Optional[datetime],
                            is_active:bool = True):
    """
    List bookings coresponding with that room  

        Args:
            number (int): number of the room to check
            is_active (bool, optional): is booking active
            date_from (date,  optional): filter from date
            date_till (date,  optional): filter till date
        Returns:
            response: List[BookingInfo]
                JSON with bookings
    """
    pass


@router.get("/rooms/{number}/requests", response_model=List[requests_schema.RequestInfo])
async def get_room_requests(number: int, 
                            date_from: Optional[datetime], date_till: Optional[datetime],
                            is_closed: bool = False):
    """
    List requests coresponding with that room  

        Args:
            number (int): number of the room to check
            is_closed (bool, optional): is request has closed
            date_from (date,  optional): filter from date
            date_till (date,  optional): filter till date
        Returns:
            response: List[RequestInfo]
                JSON with requests
    """
    pass


@router.get("/rooms/{number}/guests", response_model=List[guests_schema.GuestInfo])
async def get_room_guest(number: int):
    """
    Get who in the room now

        Args:
            number (int): number of the room to check
        Returns:
            response: List[GuestInfo]
                JSON with guest info
    """
    pass


@router.get("/roomtypes/features", response_model=List[rooms_schema.FeatureInfo])
async def get_room_type_features(offset: int = 0, limit: int = 100):
    """
    Get list of roomtype's features

        Args:
            offset (int): number for "offset" entries
            limit (int): number for "limit" entries
        Returns:
            response: List[FeatureInfo]
                JSON with roomtype's features
    """

    return await rooms_crud.get_room_type_features(offset=offset, limit=limit)


@router.post("/roomtypes/features", response_model=rooms_schema.FeatureInfo)
async def create_room_type_feature(feature: rooms_schema.FeatureCreate):
    """
    Create roomtype's feature

        Args:
            feature: FeatureCreate
                parameters required to create a roomtype
        Returns:
            response: FeatureInfo
                instance of created roomtype
    """

    return await rooms_crud.create_room_type_feature(feature=feature)


@router.delete("/roomtypes/features", response_model=rooms_schema.DeleteInfo)
async def delete_room_type_feature(id: int):
    """
    Delete roomtype's feature

        Args:
            id (int): Id of entry to delete
        Returns:
            response: DeleteInfo
                Dict with result or error
    """

    return await rooms_crud.delete_room_type_feature(id=id)


@router.post("/roomtypes/{type_id}/features", response_model=rooms_schema.FeatureTypeInfoFull)
async def add_feature_to_roomtype(type_id: int, feature_id: int):
    """
    Add feature to roomtype

        Args:
            type_id (int): id of roomtype
            feature_id (int): id of feature
        Returns:
            response: FeatureTypeInfoFull
                Dict with result
    """

    return await rooms_crud.add_feature_to_roomtype(type_id, feature_id)


@router.delete("/roomtypes/{type_id}/features", response_model=rooms_schema.DeleteInfo)
async def delete_feature_from_roomtype(type_id: int, feature_id: int):
    """
    Delete feature from roomtype

        Args:
            type_id (int): id of roomtype
            feature_id (int): id of feature
        Returns:
            response: DeleteInfo
                Dict with result
    """

    return await rooms_crud.delete_feature_from_roomtype(type_id, feature_id)


@router.get("/roomtypes/{type_id}/features", response_model=List[rooms_schema.FeatureTypeInfo])
async def get_features_to_roomtype(type_id: int):
    """
    Get roomtype's features

        Args:
            type_id (int): id of roomtype
        Returns:
            response: List[FeatureTypeInfo]
                JSON with join roomtypes and features
    """

    return await rooms_crud.get_features_to_roomtype(type_id)


@router.get("/rooms/{number}/features", response_model=List[rooms_schema.FeatureTypeInfo])
async def get_room_features(number: int):
    """
    List features corresponding with that room

        Args:
            number (int): number of the room to check
        Returns:
            response: List[FeatureTypeInfo]
                JSON with features
    """
    pass
