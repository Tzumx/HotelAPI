from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends

from crud import rooms as rooms_crud
from schemas import guests as guests_schema
from schemas import requests as requests_schema
from schemas import rooms as rooms_schema
from schemas import users as users_schema
from utils import users as users_utils

router = APIRouter()


@router.get("/roomtypes", response_model=List[rooms_schema.RoomTypeInfo],
            tags=["roomtypes"])
async def get_room_types(offset: int = 0, limit: int = 100,
                         user: users_schema.User = Depends(users_utils.get_current_user)):
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


@router.post("/roomtypes", response_model=rooms_schema.RoomTypeInfo,
             tags=["roomtypes"])
async def create_room_type(roomtype: rooms_schema.RoomTypeCreate,
                           user: users_schema.User = Depends(users_utils.get_current_user)):
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


@router.put("/roomtypes/{roomtype_id}", response_model=rooms_schema.RoomTypeInfo,
            tags=["roomtypes"])
async def update_room_type(roomtype_id: int, roomtype: rooms_schema.RoomTypeUpdate,
                           user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Update info in the room's type

        Args:
            roomtype_id (int): roomtype id for updating

            roomtype: RoomTypeCreate
                parameters required to update a roomtype
        Returns:
            response: RoomTypeInfo
                instance of updated roomtype
    """
    return await rooms_crud.update_room_type(roomtype_id, roomtype=roomtype)


@router.delete("/roomtypes/{roomtype_id}", response_model=rooms_schema.RoomDeleteInfo,
               tags=["roomtypes"])
async def delete_room_type(roomtype_id: int,
                           user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Delete room's type

        Args:
            id (int): Id of entry to delete
        Returns:
            response: DeleteInfo
                JSON with result of delete: Success or Error
    """
    return await rooms_crud.delete_room_type(id=roomtype_id)


@router.post("/rooms/filter", response_model=List[rooms_schema.RoomInfo],
             tags=["rooms"])
async def filter_rooms(filter: rooms_schema.RoomFilter = rooms_schema.RoomFilter(**{}),
                       offset: int = 0, limit: int = 100,
                       user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Get list of rooms with filter

        Args:
            offset (int, optional): number for "offset" entries
            limit (int, optional): number for "limit" entries

            room: RoomFilter
                parameters required to filter rooms
        Returns:
            response: List[RoomInfo]
                JSON with rooms
    """
    return await rooms_crud.filter_rooms(filter=filter, offset=offset, limit=limit)


@router.post("/rooms", response_model=rooms_schema.RoomInfo,
             tags=["rooms"])
async def create_room(room: rooms_schema.RoomCreate,
                      user: users_schema.User = Depends(users_utils.get_current_user)):
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


@router.put("/rooms/{number}", response_model=rooms_schema.RoomInfo,
            tags=["rooms"])
async def update_room(number: int, room: rooms_schema.RoomUpdate,
                      user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Update info in the room

        Args:
            number (int): room number

            room: RoomCreate
                parameters required to update a room
        Returns:
            response: RoomInfo
                JSON with updated room instance
    """
    return await rooms_crud.update_room(number=number, room=room)


@router.delete("/rooms/{number}", response_model=rooms_schema.RoomDeleteInfo,
               tags=["rooms"])
async def delete_room(number: int,
                      user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Delete room.

        Args:
                number (int): Id of entry to delete
        Returns:
                response: DeleteInfo
                    JSON with result of delete: Success or Error
    """
    return await rooms_crud.delete_room(number=number)


@router.get("/rooms/{number}/status", response_model=rooms_schema.RoomStatus,
            tags=["rooms"])
async def get_room_status(number: int,
                          date_from: Optional[datetime] = None,
                          date_till: Optional[datetime] = None,
                          user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Check room's status

        Args:
            number (int): number of the room to check
        Returns:
            response: RoomStatus
                JSON with status
    """
    return await rooms_crud.get_room_status(number=number, check_date_from=date_from, check_date_till=date_till)


@router.get("/rooms/{number}/requests", response_model=List[requests_schema.RequestInfo],
            tags=["rooms"])
async def get_room_requests(number: int,
                            date_from: Optional[datetime] = None,
                            date_till: Optional[datetime] = None,
                            is_closed: bool = None,
                            user: users_schema.User = Depends(users_utils.get_current_user)):
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
    return await rooms_crud.get_room_requests(number=number, date_from=date_from,
                                              date_till=date_till, is_closed=is_closed)


@router.get("/rooms/{number}/guests", response_model=List[guests_schema.GuestInfo],
            tags=["rooms"])
async def get_room_guest(number: int,
                         user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Get who in the room now

        Args:
            number (int): number of the room to check
        Returns:
            response: List[GuestInfo]
                JSON with guest info
    """
    return await rooms_crud.get_room_guest(number=number)


@router.get("/roomtypes/features", response_model=List[rooms_schema.FeatureInfo],
            tags=["roomtypes"])
async def get_room_type_features(offset: int = 0, limit: int = 100,
                                 user: users_schema.User = Depends(users_utils.get_current_user)):
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


@router.post("/roomtypes/features", response_model=rooms_schema.FeatureInfo,
             tags=["roomtypes"])
async def create_room_type_feature(feature: rooms_schema.FeatureCreate,
                                   user: users_schema.User = Depends(users_utils.get_current_user)):
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


@router.delete("/roomtypes/features/{id}", response_model=rooms_schema.RoomDeleteInfo,
               tags=["roomtypes"])
async def delete_room_type_feature(id: int,
                                   user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Delete roomtype's feature from global list

        Args:
            id (int): Id of entry to delete
        Returns:
            response: DeleteInfo
                Dict with result or error
    """

    return await rooms_crud.delete_room_type_feature(id=id)


@router.post("/roomtypes/{type_id}/features", response_model=rooms_schema.FeatureTypeInfoFull,
             tags=["roomtypes"])
async def add_feature_to_roomtype(type_id: int, feature_id: int,
                                  user: users_schema.User = Depends(users_utils.get_current_user)):
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


@router.delete("/roomtypes/{type_id}/features", response_model=rooms_schema.RoomDeleteInfo,
               tags=["roomtypes"])
async def delete_feature_from_roomtype(type_id: int, feature_id: int,
                                       user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Delete feature from roomtype

        Args:
            type_id (int): id of roomtype
            feature_id (int): id of feature
        Returns:
            response: DeleteInfo
                Dict with result (Success, Error)
    """

    return await rooms_crud.delete_feature_from_roomtype(type_id, feature_id)


@router.get("/roomtypes/{type_id}/features", response_model=List[rooms_schema.FeatureTypeInfo],
            tags=["roomtypes"])
async def get_features_to_roomtype(type_id: int,
                                   user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    Get roomtype's features

        Args:
            type_id (int): id of roomtype
        Returns:
            response: List[FeatureTypeInfo]
                JSON with join roomtypes and features
    """

    return await rooms_crud.get_features_to_roomtype(type_id)


@router.get("/rooms/{number}/features", response_model=List[rooms_schema.FeatureTypeInfo],
            tags=["rooms"])
async def get_room_features(number: int,
                            user: users_schema.User = Depends(users_utils.get_current_user)):
    """
    List features corresponding with that room

        Args:
            number (int): number of the room to check
        Returns:
            response: List[FeatureTypeInfo]
                JSON with features
    """
    return await rooms_crud.get_features_to_room(number)
