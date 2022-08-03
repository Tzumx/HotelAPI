"""Different helper-functions to work with rooms."""

from fastapi import HTTPException
from db import database
from models import rooms as rooms_model
from schemas import rooms as rooms_schema


async def create_room_type(roomtype: rooms_schema.RoomTypeCreate):
    """Create new type of room"""

    query = rooms_model.room_type.insert().values(
        type_name=roomtype.type_name, price=roomtype.price,
        description=roomtype.description)
    roomtype_id = await database.execute(query)
    return {**roomtype.dict(), "id": roomtype_id}


async def delete_room_type(id: int):
    """Delete room's type by id"""

    query = rooms_model.room_type.select().where(
                                            rooms_model.room_type.c.id == id)
    answer = await database.execute(query)
    if answer == id:
        query = rooms_model.room_type.delete().where(
                                            rooms_model.room_type.c.id == id)
        await database.execute(query)
        answer = "Success"
    else:
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}


async def get_room_types(offset: int = 0, limit: int = 100):
    """Get list of room's types"""

    results = await database.fetch_all(rooms_model.room_type.select(
    ).offset(offset).limit(limit))
    return [dict(result._mapping) for result in results]


async def create_room_type_feature(roomtype_feature: rooms_schema.FeatureCreate):
    """Create new feature for roomtype"""

    query = rooms_model.feature.insert().values(
        feature=roomtype_feature.feature)
    feature_id = await database.execute(query)
    if feature_id != None:
        return {**roomtype_feature.dict(), "id": feature_id}
    else:
        HTTPException(status_code=409, detail="Already exist")


async def delete_room_type_feature(id: int):
    """Delete roomtype's feature by id"""

    query = rooms_model.feature.select().where(rooms_model.feature.c.id == id)
    answer = await database.execute(query)
    if answer == id:
        query = rooms_model.feature.delete().where(rooms_model.feature.c.id == id)
        await database.execute(query)
        answer = "Success"
    else:
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}


async def get_room_type_features(offset: int = 0, limit: int = 100):
    """Get list of roomtype's features"""

    results = await database.fetch_all(rooms_model.feature.select(
    ).offset(offset).limit(limit))
    return [dict(result._mapping) for result in results]


async def add_feature_to_roomtype(fk_room_type_id: int, fk_feature_id: int):
    """Add feature to roomtype"""

    query = rooms_model.roomtype_feature.select(
                ).where(rooms_model.roomtype_feature.c.fk_room_type_id == fk_room_type_id
                ).where(rooms_model.roomtype_feature.c.fk_feature_id == fk_feature_id)
    answer = await database.execute(query)
    if answer != None:
        raise HTTPException(status_code=409, detail="Already exist")

    query = rooms_model.roomtype_feature.insert().values(
        fk_room_type_id=fk_room_type_id, fk_feature_id=fk_feature_id)
    err = await database.execute(query)
    if err != None:
        raise HTTPException(status_code=409, detail=err)

    sum_table = rooms_model.roomtype_feature.join(rooms_model.room_type,
                rooms_model.roomtype_feature.c.fk_room_type_id == rooms_model.room_type.c.id
                ).join(rooms_model.feature,
                rooms_model.roomtype_feature.c.fk_feature_id == rooms_model.feature.c.id)
    result = await database.fetch_one(sum_table.select().
                                      where(rooms_model.room_type.c.id == fk_room_type_id).
                                      where(rooms_model.feature.c.id == fk_feature_id).
                                      with_only_columns(
                                      [rooms_model.room_type.c.type_name,
                                       rooms_model.room_type.c.price,
                                       rooms_model.room_type.c.description,
                                       rooms_model.feature.c.feature]))
    return dict(result._mapping)


async def delete_feature_from_roomtype(fk_room_type_id: int, fk_feature_id: int):
    """Delete roomtype's feature by id"""

    query = rooms_model.roomtype_feature.select().where(
        rooms_model.roomtype_feature.c.fk_room_type_id == fk_room_type_id
    ).where(
        rooms_model.roomtype_feature.c.fk_feature_id == fk_feature_id)
    answer = await database.execute(query)
    if answer != None:
        query = rooms_model.roomtype_feature.delete().where(
            rooms_model.roomtype_feature.c.fk_room_type_id == fk_room_type_id
        ).where(
            rooms_model.roomtype_feature.c.fk_feature_id == fk_feature_id)
        await database.execute(query)
        answer = "Success"
    else:
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}


async def get_features_to_roomtype(fk_room_type_id: int):
    """Get list of roomtype's features"""

    sum_table = rooms_model.roomtype_feature.join(rooms_model.room_type,
                    rooms_model.roomtype_feature.c.fk_room_type_id == rooms_model.room_type.c.id
                    ).join(rooms_model.feature,
                    rooms_model.roomtype_feature.c.fk_feature_id == rooms_model.feature.c.id)
    results = await database.fetch_all(sum_table.select().
                                where(rooms_model.room_type.c.id == fk_room_type_id).
                                with_only_columns([rooms_model.feature.c.feature]))
    return [dict(result._mapping) for result in results]


async def create_room(room: rooms_schema.RoomCreate):
    """Create new room"""

    query = rooms_model.room.select().where(
                                    rooms_model.room.c.number == room.number)
    answer = await database.execute(query)
    if answer == None:
        query = rooms_model.room.insert().values(number=room.number,
                                    type_id=room.type_id, floor=room.floor,
                                    housing=room.housing)
        room_id = await database.execute(query)
        return {**room.dict()}
    else:
        raise HTTPException(status_code=409, detail="Already exist")


async def delete_room(number: int):
    """Delete room by id"""

    query = rooms_model.room.select().where(rooms_model.room.c.number == number)
    answer = await database.execute(query)
    if answer == number:
        query = rooms_model.room.delete().where(
                                            rooms_model.room.c.number == number)
        await database.execute(query)
        answer = "Success"
    else:
        answer = "Error"
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}


async def get_rooms(offset: int = 0, limit: int = 100):
    """Get list of rooms"""

    results = await database.fetch_all(
                        rooms_model.room.select().offset(offset).limit(limit))
    return [dict(result._mapping) for result in results]
