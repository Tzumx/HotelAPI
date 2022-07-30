from datetime import datetime
from fastapi import APIRouter
from typing import List

from schemas import rooms as rooms_schema
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
async def update_room_type(roomtype: rooms_schema.RoomTypeInfo):
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


@router.delete("/roomtypes", response_model=rooms_schema.DeleteInfo)
async def delete_room_type(id: int):
    """
    Delete room's type

        Args:
                id (int): Id of entry to delete
        Returns:
                response: DeleteInfo
                        JSON with result of delete: Success or Error
    """
    return await rooms_crud.delete_room_type(id=id)


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
async def filter_rooms(room: rooms_schema.RoomInfo,
                       offset: int = 0, limit: int = 100):
    """
    Get list of rooms with filter

        Args:
                offset (int, optional): number for "offset" entries
                limit (int, optional): number for "limit" entries
                room: RoomInfo
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
                        JSON with result of creation or error
    """
    return await rooms_crud.create_room(room=room)


@router.put("/rooms/{room_id}", response_model=rooms_schema.RoomInfo)
async def update_room(room: rooms_schema.RoomInfo):
    """
    Update info in the room

        Args:
                room: RoomInfo
                        parameters required to update a room
        Returns:
                response: RoomInfo
                        JSON with result of update or error
    """
    return await rooms_crud.update_room(room=room)


@router.delete("/rooms", response_model=rooms_schema.DeleteInfo)
async def delete_room(number: int):
    """
    Delete room.

        Args:
                id (int): Id of entry to delete
        Returns:
                response: DeleteInfo
                        JSON with result of delete: Success or Error
    """
    return await rooms_crud.delete_room(number=number)


@router.get("/rooms/{room_number}/status")  # add response model
async def room_status(date_from: datetime, date_till: datetime):
    """
    Check room's status inside a date range   

        Args:
                room_number (int): number of the room to check
                date_from (datetime): filter date from
                date_till (datetime): filter date till
        Returns:
                JSON with answer (true or false)
    """
    pass


@router.get("/rooms/{room_number}/bookings")  # add response model
async def get_room_bookings(date_from: datetime, date_till: datetime):
    """
    List bookings coresponding with that room  

        Args:
                room_number (int): number of the room to check
                date_from (date,  optional): filter from date
                date_till (date,  optional): filter till date
        Returns:
                JSON with bookings or error
    """
    pass


@router.get("/rooms/{room_number}/requests")  # add response model
async def get_room_requests(is_closed: bool, date_from: datetime, date_till: datetime):
    """
    List requests coresponding with that room  

        Args:
                room_number (int): number of the room to check
                is_closed (bool): is request has closed
                date_from (date,  optional): filter from date
                date_till (date,  optional): filter till date
        Returns:
                JSON with requests or error
    """
    pass


@router.get("/rooms/{room_number}/guests")  # add response model
async def get_room_guest(room_number: int):
    """
    Get who in the room now

        Args:
                room_number (int): number of the room to check
        Returns:
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
async def create_room_type_feature(roomtype_feature: rooms_schema.FeatureCreate):
    """
    Create roomtype's feature

        Args:
                roomtype_feature: FeatureCreate
                      parameters required to create a roomtype
        Returns:
                response: FeatureInfo
                      instance of created roomtype
    """
    return await rooms_crud.create_room_type_feature(roomtype_feature=roomtype_feature)


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
async def delete_feature_from_roomtype(fk_room_type_id: int, feature_id: int):
    """
    Delete feature from roomtype

        Args:
                room_type_id (int): id of roomtype
                feature_id (int): id of feature
        Returns:
                response: DeleteInfo
                      Dict with result
    """
    return await rooms_crud.delete_feature_from_roomtype(fk_room_type_id, feature_id)


@router.get("/roomtypes/{type_id}/features", response_model=List[rooms_schema.FeatureTypeInfo])
async def get_features_to_roomtype(fk_room_type_id: int):
    """
    Get roomtype's features

        Args:
                room_type_id (int): id of roomtype
                feature_id (int): id of feature
        Returns:
                response: List[FeatureTypeInfo]
                      JSON with join roomtypes and features
    """
    return await rooms_crud.get_features_to_roomtype(fk_room_type_id)


@router.get("/rooms/{room_number}/features")  # add response model
async def get_room_features(room_number: int):  # add schema or query params
    """
    List features corresponding with that room

        Args:
                room_number (int): number of the room to check
        Returns:
                JSON with features
    """
    pass
