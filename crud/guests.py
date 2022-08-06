"""Different crud-functions to work with guests."""

from fastapi import HTTPException
from db import database
from models import guests as guests_model, bookings as bookings_model, requests as requests_model
from schemas import guests as guests_schema


async def filter_guests(filter: guests_schema.GuestFilter, offset: int = 0, limit: int = 100):
    """Get filter list of guests"""

    filter_query = guests_model.guest.select()
    if not filter.name == None:
        filter_query = filter_query.where(
            guests_model.guest.c.name == filter.name)
    if not filter.email == None:
        filter_query = filter_query.where(
            guests_model.guest.c.email == filter.email)
    if not filter.phone == None:
        filter_query = filter_query.where(
            guests_model.guest.c.phone == filter.phone)

    results = await database.fetch_all(filter_query.order_by(guests_model.guest.c.id))

    return [dict(result._mapping) for result in results]


async def create_guest(guest: guests_schema.GuestCreate):
    """Create new guest"""

    query = guests_model.guest.insert().values(name=guest.name,
                                               email=guest.email, phone=guest.phone)
    guest_id = await database.execute(query)
    return {**guest.dict(), "id": guest_id}


async def update_guest(guest_id, guest: guests_schema.GuestCreate):
    """Update the guest"""

    query = guests_model.guest.select().where(guests_model.guest.c.id == guest_id)
    answer = await database.execute(query)
    if answer == guest_id:
        query = guests_model.guest.update().values(
            name=guest.name,
            email=guest.email,
            phone=guest.phone).where(
            guests_model.guest.c.id == guest_id)
        await database.execute(query)
        return {**guest.dict(), "id": guest_id}
    else:
        raise HTTPException(status_code=404, detail="Not found")


async def delete_guest(guest_id: int):
    """Delete guest by id"""

    query = guests_model.guest.select().where(guests_model.guest.c.id == guest_id)
    answer = await database.execute(query)
    if answer == guest_id:
        query = guests_model.guest.delete().where(
            guests_model.guest.c.id == guest_id)
        await database.execute(query)
        answer = "Success"
    else:
        answer = "Error"
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}


async def get_guest_requests(guest_id: int, is_closed: bool = False):
    """List requests connected with this guest"""

    query = bookings_model.booking.select().where(
        bookings_model.booking.c.fk_guest_id == guest_id)
    answer = await database.fetch_all(query)
    bookings = [dict(result._mapping)['id'] for result in answer]
    query = requests_model.request.select().where(
        requests_model.request.c.fk_booking_id.in_(bookings))
    results = await database.fetch_all(query)

    return [dict(result._mapping) for result in results]
