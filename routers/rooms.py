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
                description (str): description
        Returns:
                Dict with result
    """
    return await rooms_crud.create_room_type(roomtype=roomtype)


@router.delete("/roomtypes", response_model=rooms_schema.DeleteInfo)
async def delete_room_type(id: int):
    """
    Delete room's type

        Args:
                id (int): Id of entry to delete
        Returns:
                Dict with result or error
    """
    return await rooms_crud.delete_room_type(id=id)


@router.get("/roomtypes", response_model=List[rooms_schema.RoomTypeInfo])
async def get_room_types(offset: int = 0, limit: int = 100):
    """
    Get list of room's types

        Args:
                offset (int): number for "offset" entries
                limit (int): number for "limit" entries
        Returns:
                JSON with room's types
    """
    return await rooms_crud.get_room_types(offset=offset, limit=limit)


@router.post("/roomtypes/features", response_model=rooms_schema.FeatureInfo)
async def create_room_type_feature(roomtype_feature: rooms_schema.FeatureCreate):
    """
    Create roomtype's feature

        Args:
                feature (str): name of feature
        Returns:
                Dict with result
    """
    return await rooms_crud.create_room_type_feature(roomtype_feature=roomtype_feature)


@router.delete("/roomtypes/features", response_model=rooms_schema.DeleteInfo)
async def delete_room_type_feature(id: int):
    """
    Delete roomtype's feature

        Args:
                id (int): Id of entry to delete
        Returns:
                Dict with result or error
    """
    return await rooms_crud.delete_room_type_feature(id=id)


@router.get("/roomtypes/features", response_model=List[rooms_schema.FeatureInfo])
async def get_room_type_features(offset: int = 0, limit: int = 100):
    """
    Get list of roomtype's features

        Args:
                offset (int): number for "offset" entries
                limit (int): number for "limit" entries
        Returns:
                JSON with roomtype's features
    """
    return await rooms_crud.get_room_type_features(offset=offset, limit=limit)


@router.post("/roomtypes/{type_id}/feature", response_model=rooms_schema.FeatureTypeInfoFull)
async def add_feature_to_roomtype(type_id: int, feature_id: int):
    """
    Add feature to roomtype

        Args:
                type_id (int): id of roomtype
                feature_id (int): id of feature
        Returns:
                Dict with result
    """
    return await rooms_crud.add_feature_to_roomtype(type_id, feature_id)


@router.delete("/roomtypes/{type_id}/feature", response_model=rooms_schema.DeleteInfo)
async def delete_feature_from_roomtype(fk_room_type_id: int, feature_id: int):
    """
    Delete feature from roomtype

        Args:
                fk_room_type_id (int): id of roomtype
                fk_feature_id (int): id of feature
        Returns:
                Dict with result

    """
    return await rooms_crud.delete_feature_from_roomtype(fk_room_type_id, feature_id)


@router.get("/roomtypes/{type_id}/feature", response_model=List[rooms_schema.FeatureTypeInfo])
async def get_features_to_roomtype(fk_room_type_id: int):
    """
    Get roomtype's feature

        Args:
                fk_room_type_id (int): id of roomtype
                fk_feature_id (int): id of feature
        Returns:
                JSON with join roomtypes and features
    """
    return await rooms_crud.get_features_to_roomtype(fk_room_type_id)


@router.post("/rooms", response_model=rooms_schema.RoomInfo)
async def create_room(room: rooms_schema.RoomCreate):
    """
    Add new room

        Args:
                number (int): room number
                fk_room_types_id (int): room's type
                floor (int): the room is located on this floor, default = 0
                housing (int): number of housing, default = 0
        Returns:
                Dict with result of creation or error
    """
    return await rooms_crud.create_room(room=room)


@router.delete("/rooms", response_model=rooms_schema.DeleteInfo)
async def delete_room(number: int):
    """
    Delete room.

        Args:
                number (int): number of room to delete
        Returns:
                Dict with result
    """
    return await rooms_crud.delete_room(number=number)


@router.get("/rooms", response_model=List[rooms_schema.RoomInfo])
async def get_rooms(offset: int = 0, limit: int = 100):
    """
    Get list of rooms

        Args:
                offset (int): number for "offset" entries
                limit (int): number for "limit" entries
        Returns:
                JSON with rooms
    """
    return await rooms_crud.get_rooms(offset=offset, limit=limit)
