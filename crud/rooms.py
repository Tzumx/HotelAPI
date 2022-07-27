"""Different helper-functions to work with rooms."""

# from datetime import datetime, timedelta
from fastapi import HTTPException
from db import database
from models.rooms import room_table, room_type_table, roomtype_feature, room_feature
from schemas import rooms as rooms_schema


async def create_room_type(roomtype: rooms_schema.RoomTypeCreate):
    """Create new type of room"""

    query = room_type_table.insert().values(
        type_name=roomtype.type_name, price=roomtype.price,
        description=roomtype.description)
    roomtype_id = await database.execute(query)
    return {**roomtype.dict(), "id": roomtype_id}


async def delete_room_type(id: int):
    """Delete room's type by id"""

    query = room_type_table.select().where(room_type_table.c.id == id)
    answer = await database.execute(query)
    if answer == id:
        query = room_type_table.delete().where(room_type_table.c.id == id)
        await database.execute(query)
        answer = "Success"
    else:
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}


async def get_room_types(offset: int = 0, limit: int = 100):
    """Get list of room's types"""

    results = await database.fetch_all(room_type_table.select(
                                       ).offset(offset).limit(limit))
    return [dict(result._mapping) for result in results]


async def create_room_type_feature(roomtype_feature: rooms_schema.FeatureCreate):
    """Create new feature for roomtype"""

    query = room_feature.insert().values(
        feature=roomtype_feature.feature)
    feature_id = await database.execute(query)
    if feature_id != None:
        return {**roomtype_feature.dict(), "id": feature_id}
    else:
        HTTPException(status_code=409, detail="Already exist")


async def delete_room_type_feature(id: int):
    """Delete roomtype's feature by id"""

    query = room_feature.select().where(room_feature.c.id == id)
    answer = await database.execute(query)
    if answer == id:
        query = room_feature.delete().where(room_feature.c.id == id)
        await database.execute(query)
        answer = "Success"
    else:
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}


async def get_room_type_features(offset: int = 0, limit: int = 100):
    """Get list of roomtype's features"""

    results = await database.fetch_all(room_feature.select(
                                       ).offset(offset).limit(limit))
    return [dict(result._mapping) for result in results]


async def add_feature_to_roomtype(type_id: int, feature_id: int):
    """Add feature to roomtype"""

    query = roomtype_feature.select().where(roomtype_feature.c.type_id == type_id
                                   ).where(roomtype_feature.c.feature_id == feature_id)
    answer = await database.execute(query)
    if answer != None:
        raise HTTPException(status_code=409, detail="Already exist")

    query = roomtype_feature.insert().values(
        type_id=type_id, feature_id=feature_id)
    err = await database.execute(query)
    if err != None:
        raise HTTPException(status_code=409, detail=err)

    sum_table = roomtype_feature.join(room_type_table,
                    roomtype_feature.c.type_id == room_type_table.c.id).join(
                    room_feature, roomtype_feature.c.feature_id == room_feature.c.id)
    result = await database.fetch_one(sum_table.select().
                                      where(room_type_table.c.id == type_id).
                                      where(room_feature.c.id == feature_id).
                                      with_only_columns(
                                      [room_type_table.c.type_name,
                                      room_type_table.c.price, 
                                      room_type_table.c.description,
                                      room_feature.c.feature]))
    return dict(result._mapping)


async def delete_feature_from_roomtype(type_id: int, feature_id: int):
    """Delete roomtype's feature by id"""

    query = roomtype_feature.select().where(
                                    roomtype_feature.c.type_id == type_id
                                    ).where(
                                    roomtype_feature.c.feature_id == feature_id)
    answer = await database.execute(query)
    if answer != None:
        query = roomtype_feature.delete().where(
                                        roomtype_feature.c.type_id == type_id
                                        ).where(
                                        roomtype_feature.c.feature_id == feature_id)
        await database.execute(query)
        answer = "Success"
    else:
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}


async def get_feature_to_roomtype(type_id: int):
    """Get list of roomtype's features"""

    sum_table = roomtype_feature.join(room_type_table,
                                      roomtype_feature.c.type_id == room_type_table.c.id
                                      ).join(room_feature,
                                      roomtype_feature.c.feature_id == room_feature.c.id)
    results = await database.fetch_all(sum_table.select().
                                       where(room_type_table.c.id == type_id).
                                       with_only_columns([room_feature.c.feature]))
    return [dict(result._mapping) for result in results]


async def create_room(room: rooms_schema.RoomCreate):
    """Create new room"""

    query = room_table.select().where(room_table.c.number == room.number)
    answer = await database.execute(query)
    if answer == None:
        query = room_table.insert().values(
            number=room.number, type_id=room.type_id, is_clean=room.is_clean)
        room_id = await database.execute(query)
        return {**room.dict(), "id": room_id}
    else:
        raise HTTPException(status_code=409, detail="Already exist")


async def delete_room(id: int):
    """Delete room by id"""

    query = room_table.select().where(room_table.c.id == id)
    answer = await database.execute(query)
    if answer == id:
        query = room_table.delete().where(room_table.c.id == id)
        await database.execute(query)
        answer = "Success"
    else:
        answer = "Error"
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}


async def get_rooms(offset: int = 0, limit: int = 100):
    """Get list of rooms"""

    results = await database.fetch_all(room_table.select().offset(offset).limit(limit))
    return [dict(result._mapping) for result in results]
