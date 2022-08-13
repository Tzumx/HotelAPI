"""Different helper-functions to work with rooms."""

from datetime import datetime

from fastapi import HTTPException, Query

from db import database
from models import bookings as bookings_model
from models import guests as guests_model
from models import requests as requests_model
from models import rooms as rooms_model
from schemas import rooms as rooms_schema


async def get_room_types(offset: int = 0, limit: int = 100):
    """Get list of room's types"""

    results = await database.fetch_all(
        rooms_model.room_type.select().offset(offset).limit(limit))
    return [dict(result._mapping) for result in results]


async def create_room_type(roomtype: rooms_schema.RoomTypeCreate):
    """Create new type of room"""

    query = rooms_model.room_type.insert().values(
        type_name=roomtype.type_name, price=roomtype.price,
        description=roomtype.description)
    roomtype_id = await database.execute(query)
    return {**roomtype.dict(), "id": roomtype_id}


async def update_room_type(roomtype_id, roomtype: rooms_schema.RoomTypeUpdate):
    """Update the type of room"""

    query = rooms_model.room_type.select().where(
        rooms_model.room_type.c.id == roomtype_id)
    stored_data = await database.fetch_one(query)
    if stored_data != None:
        stored_data = dict(stored_data._mapping)
        update_data = roomtype.dict(exclude_unset=True)
        stored_data.update(update_data)
        query = rooms_model.room_type.update().values(**stored_data).where(
            rooms_model.room_type.c.id == roomtype_id)
        await database.execute(query)
        return {**stored_data, "id": roomtype_id}
    else:
        raise HTTPException(status_code=404, detail="Not found")


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


async def filter_rooms(filter: rooms_schema.RoomFilter, offset: int = 0, limit: int = 100):
    """Get filter list of rooms"""

    filter_params = filter.dict(exclude_unset=True)
    filter_features = filter_params.pop('features', [])

    filter_query = rooms_model.room.select()

    for k, v in filter_params.items():
        filter_query = filter_query.where(rooms_model.room.c[k] == v)

    results = await database.fetch_all(filter_query.order_by(rooms_model.room.c.number))

    answer = []
    for result in results:
        current_room = dict(result._mapping)
        features_list = await get_features_to_room(current_room['number'])
        features_list = [elem['feature'] for elem in features_list]
        if all(elem in features_list for elem in filter_features):
            current_room["features"] = features_list
            answer.append(current_room)

    return answer


async def create_room(room: rooms_schema.RoomCreate):
    """Create new room"""

    query = rooms_model.room.select().where(
        rooms_model.room.c.number == room.number)
    answer = await database.execute(query)
    if answer == None:
        query = rooms_model.room.insert().values(number=room.number,
                                                 fk_room_types_id=room.room_types_id, floor=room.floor,
                                                 housing=room.housing)
        room_id = await database.execute(query)
        return {**room.dict()}
    else:
        raise HTTPException(status_code=409, detail="Already exist")


async def update_room(number, room: rooms_schema.RoomUpdate):
    """Update the room"""

    query = rooms_model.room.select().where(rooms_model.room.c.number == number)
    stored_data = await database.fetch_one(query)
    if stored_data != None:
        stored_data = dict(stored_data._mapping)
        update_data = room.dict(exclude_unset=True)
        stored_data.update(update_data)
        query = rooms_model.room.update().values(**stored_data).where(
            rooms_model.room.c.number == number)
        await database.execute(query)
        return {**stored_data, "number": number}
    else:
        raise HTTPException(status_code=404, detail="Not found")


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


async def create_room_type_feature(feature: rooms_schema.FeatureCreate):
    """Create new feature for roomtype"""

    query = rooms_model.feature.insert().values(
        feature=feature.feature)
    feature_id = await database.execute(query)
    if feature_id != None:
        return {**feature.dict(), "id": feature_id}
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


async def delete_feature_from_roomtype(type_id: int, feature_id: int):
    """Delete roomtype's feature by id"""

    query = rooms_model.roomtype_feature.select().where(
        rooms_model.roomtype_feature.c.fk_room_type_id == type_id
    ).where(
        rooms_model.roomtype_feature.c.fk_feature_id == feature_id)
    answer = await database.execute(query)
    if answer != None:
        query = rooms_model.roomtype_feature.delete().where(
            rooms_model.roomtype_feature.c.fk_room_type_id == type_id
        ).where(
            rooms_model.roomtype_feature.c.fk_feature_id == feature_id)
        await database.execute(query)
        answer = "Success"
    else:
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}


async def get_features_to_roomtype(room_type_id: int):
    """Get list of roomtype's features"""

    sum_table = rooms_model.roomtype_feature.join(rooms_model.room_type,
                                                  rooms_model.roomtype_feature.c.fk_room_type_id == rooms_model.room_type.c.id
                                                  ).join(rooms_model.feature,
                                                         rooms_model.roomtype_feature.c.fk_feature_id == rooms_model.feature.c.id)
    results = await database.fetch_all(sum_table.select().
                                       where(rooms_model.room_type.c.id == room_type_id).
                                       with_only_columns([rooms_model.feature.c.feature]))
    return [dict(result._mapping) for result in results]


async def get_features_to_room(number: int):
    """Get list of room's features"""

    query = rooms_model.room.select().where(rooms_model.room.c.number == number)
    room = await database.fetch_all(query)
    if len(room) > 0:
        fk = room[0].fk_room_types_id
        return await get_features_to_roomtype(fk)
    else:
        raise HTTPException(status_code=404, detail="Not found")


async def get_room_guest(number: int):
    """Get who in the room now"""

    now = datetime.now()
    query = bookings_model.booking.select().where(
        bookings_model.booking.c.fk_room_number == number).where(
        bookings_model.booking.c.is_active == True).where(
        bookings_model.booking.c.check_in < now).where(
        bookings_model.booking.c.check_out > now)
    booking = await database.fetch_all(query)
    if len(booking) > 0:
        fk = booking[0].fk_guest_id
        query = guests_model.guest.select().where(guests_model.guest.c.id == fk)
        result = await database.fetch_one(query)
        return [dict(result._mapping)]
    else:
        raise HTTPException(status_code=404, detail="Not found")


async def get_room_requests(number: int,
                            date_from: datetime, date_till: datetime,
                            is_closed: bool):
    """List requests coresponding with that room"""

    query = bookings_model.booking.select().where(
        bookings_model.booking.c.fk_room_number == number)
    answer = await database.fetch_all(query)
    bookings = [dict(result._mapping)['id'] for result in answer]
    query = requests_model.request.select().where(
        requests_model.request.c.fk_booking_id.in_(bookings))
    if not date_from == None:
        query = query.where(requests_model.request.c.created_at > date_from)
    if not date_till == None:
        query = query.where(requests_model.request.c.created_at < date_till)
    if is_closed != True:
        query = query.where(requests_model.request.c.is_closed == False)
    results = await database.fetch_all(query)

    return [dict(result._mapping) for result in results]


async def get_room_status(number: int, check_date_from: datetime,
                          check_date_till: datetime):
    """Check room's status"""

    if check_date_from == None or check_date_till == None:
        check_date_from = check_date_till = datetime.now()
    status = {"is_free": True, "is_open_requests": False}
    query = bookings_model.booking.select().where(
        bookings_model.booking.c.fk_room_number == number)
    answer = await database.fetch_all(query)
    bookings = [dict(result._mapping) for result in answer]
    for booking in bookings:
        if booking['is_active'] == True:
            if (check_date_from <= booking['check_in'] and
                check_date_till >= booking["check_out"]) or \
               (check_date_from >= booking['check_in']
                and check_date_from <= booking["check_out"]) or \
               (check_date_till >= booking['check_in']
                    and check_date_till <= booking["check_out"]):
                status["is_free"] = False
                if "is_paid" not in status.keys() or status['is_paid'] == True:
                    status['is_paid'] = booking['is_paid']

    requests = await get_room_requests(number, None, None, False)
    if len(requests) > 0:
        status['is_open_requests'] = True

    return status
