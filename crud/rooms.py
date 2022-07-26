"""Different helper-functions to work with rooms."""

# from datetime import datetime, timedelta
from http.client import HTTPException
from db import database
from models.rooms import room_table, room_type_table
from schemas import rooms as rooms_schema


async def create_room_types(roomtype: rooms_schema.RoomTypeCreate):
    """Create new type of room"""
    query = room_type_table.insert().values(
        type=roomtype.type, price=roomtype.price,
        description=roomtype.description, is_doublebad=roomtype.is_doublebad,
        is_kitchen=roomtype.is_kitchen, is_bathroom=roomtype.is_bathroom,
        is_conditioner=roomtype.is_conditioner, is_TV=roomtype.is_TV)
    roomtype_id = await database.execute(query)
    return {**roomtype.dict(), "id": roomtype_id}


async def delete_room_types(id: int):
    """Delete room's type by id"""
    query = room_type_table.select().where(room_type_table.c.id == id)
    answer = await database.execute(query)
    if answer == id:
        query = room_type_table.delete().where(room_type_table.c.id == id)
        await database.execute(query)
        answer = "Success"
    else:
        answer = "Error"
    return {"result": answer}


async def get_room_types(skip: int = 0, limit: int = 100):
    """Get list of room's types"""
    results = await database.fetch_all(room_type_table.select().offset(skip).limit(limit))
    return [dict(result._mapping) for result in results]


async def create_rooms(room: rooms_schema.RoomCreate):
    """Create new room"""
    query = room_table.select().where(room_table.c.number == room.number)
    answer = await database.execute(query)
    if answer == None:
        query = room_table.insert().values(
            number=room.number, type_id=room.type_id, is_clean=room.is_clean)
        room_id = await database.execute(query)
        return {**room.dict(), "id": room_id}
    else: return {"result": "Error"}


async def delete_rooms(id: int):
    """Delete room by id"""
    query = room_table.select().where(room_table.c.id == id)
    answer = await database.execute(query)
    if answer == id:
        query = room_table.delete().where(room_table.c.id == id)
        await database.execute(query)
        answer = "Success"
    else:
        answer = "Error"
        # raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}


async def get_rooms(skip: int = 0, limit: int = 100):
    """Get list of rooms"""
    results = await database.fetch_all(room_table.select().offset(skip).limit(limit))
    return [dict(result._mapping) for result in results]
