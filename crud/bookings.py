"""Different crud-functions to work with bookings."""

from fastapi import HTTPException

from crud import rooms as room_crud
from db import database
from models import bookings as bookings_model
from models import requests as requests_model
from models import rooms as rooms_model
from schemas import bookings as bookings_schema


async def filter_bookings(filter: bookings_schema.BookingFilter,
                          offset: int = 0, limit: int = 100):
    """Get filter list of bookings"""

    filter_query = bookings_model.booking.select()
    if not filter.room_number == None:
        filter_query = filter_query.where(
            bookings_model.booking.c.fk_room_number == filter.room_number)
    if not filter.guest_id == None:
        filter_query = filter_query.where(
            bookings_model.booking.c.fk_guest_id == filter.guest_id)
    if not filter.is_paid == None:
        filter_query = filter_query.where(
            bookings_model.booking.c.is_paid == filter.is_paid)
    if not filter.is_active == None:
        filter_query = filter_query.where(
            bookings_model.booking.c.is_active == filter.is_active)
    if not filter.check_in_from == None:
        filter_query = filter_query.where(
            bookings_model.booking.c.check_in >= filter.check_in_from)
    if not filter.check_in_till == None:
        filter_query = filter_query.where(
            bookings_model.booking.c.check_in <= filter.check_in_till)
    if not filter.check_out_from == None:
        filter_query = filter_query.where(
            bookings_model.booking.c.check_out >= filter.check_out_from)
    if not filter.check_out_till == None:
        filter_query = filter_query.where(
            bookings_model.booking.c.check_out <= filter.check_out_till)

    results = await database.fetch_all(filter_query.order_by(bookings_model.booking.c.id))

    return [dict(result._mapping) for result in results]


async def create_booking(booking: bookings_schema.BookingCreate):
    """Create new booking"""

    is_free = await room_crud.get_room_status(booking.room_number, booking.check_in, booking.check_out)
    is_free = is_free["is_free"]
    if is_free == False:
        raise HTTPException(status_code=409, detail="Room is not free")

    query = bookings_model.booking.insert().values(fk_room_number=booking.room_number,
                                                   fk_guest_id=booking.guest_id,
                                                   check_in=booking.check_in,
                                                   check_out=booking.check_out,
                                                   description=booking.description)
    booking_id = await database.execute(query)
    query = bookings_model.booking.select().where(
        bookings_model.booking.c.id == booking_id)
    results = await database.fetch_one(query)
    return dict(results._mapping)


async def update_booking(booking_id, booking: bookings_schema.BookingUpdate):
    """Update the booking"""

    query = bookings_model.booking.select().where(
        bookings_model.booking.c.id == booking_id)
    stored_data = await database.fetch_one(query)
    if stored_data != None:
        stored_data = dict(stored_data._mapping)
        update_data = booking.dict(exclude_unset=True)
        stored_data.update(update_data)
        query = bookings_model.booking.update().values(**stored_data).where(
            bookings_model.booking.c.id == booking_id)
        await database.execute(query)
        return {**stored_data, "id": booking_id}
    else:
        raise HTTPException(status_code=404, detail="Not found")


async def delete_booking(booking_id: int):
    """Delete booking by id"""

    query = bookings_model.booking.select().where(
        bookings_model.booking.c.id == booking_id)
    answer = await database.execute(query)
    if answer == booking_id:
        query = bookings_model.booking.delete().where(
            bookings_model.booking.c.id == booking_id)
        await database.execute(query)
        answer = "Success"
    else:
        answer = "Error"
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}


async def set_booking_status(booking_id: int, is_active: bool):
    """Set booking state"""

    query = bookings_model.booking.select().where(
        bookings_model.booking.c.id == booking_id)
    answer = await database.execute(query)
    if answer == booking_id:
        query = bookings_model.booking.update().values(is_active=is_active).where(
            bookings_model.booking.c.id == booking_id)
        await database.execute(query)
        query = bookings_model.booking.select().where(
            bookings_model.booking.c.id == booking_id)
        answer = await database.fetch_all(query)
        return dict(answer[0]._mapping)
    else:
        raise HTTPException(status_code=404, detail="Not found")


async def post_booking_review(booking_id: int, review: bookings_schema.BookingReview):
    """Update client's review"""

    query = bookings_model.booking.select().where(
        bookings_model.booking.c.id == booking_id)
    answer = await database.execute(query)
    if answer == booking_id:
        query = bookings_model.booking.update().values(client_review=review.review).where(
            bookings_model.booking.c.id == booking_id)
        await database.execute(query)
        query = bookings_model.booking.select().where(
            bookings_model.booking.c.id == booking_id)
        answer = await database.fetch_all(query)
        return dict(answer[0]._mapping)
    else:
        raise HTTPException(status_code=404, detail="Not found")


async def get_booking_sum(booking_id: int):
    """Get full price for the booking"""

    results = await database.fetch_one(bookings_model.booking.select().where(
        bookings_model.booking.c.id == booking_id))
    if results == None:
        raise HTTPException(status_code=404, detail="Not found")
    room_number = dict(results._mapping)['fk_room_number']
    results = await database.fetch_one(rooms_model.room.select().where(
        rooms_model.room.c.number == room_number))
    room_type = dict(results._mapping)['fk_room_types_id']
    results = await database.fetch_one(rooms_model.room_type.select().where(
        rooms_model.room_type.c.id == room_type))
    price = dict(results._mapping)['price']
    results = await database.fetch_all(requests_model.request.select().where(
        requests_model.request.c.fk_booking_id == booking_id))
    for request_booking in results:
        price += dict(request_booking._mapping)['price']

    return {"sum": price}
