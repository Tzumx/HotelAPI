"""Different crud-functions to work with payments."""

from fastapi import HTTPException
from db import database
from models import payments as payments_model, bookings as bookings_model, rooms as rooms_model
from schemas import payments as payments_schema


async def get_payments(offset: int = 0, limit: int = 100):
    """Get list of payments"""

    results = await database.fetch_all(payments_model.payment.select(
    ).offset(offset).limit(limit))
    return [dict(result._mapping) for result in results]


async def filter_payments(filter: payments_schema.PaymentFilter,
                          offset: int = 0, limit: int = 100):
    """Get filter list of payments"""

    filter_query = payments_model.payment.select()
    if not filter.booking_id == None:
        filter_query = filter_query.where(
            payments_model.payment.c.fk_booking_id == filter.booking_id)
    if not filter.sum_from == None:
        filter_query = filter_query.where(
            payments_model.payment.c.sum >= filter.sum_from)
    if not filter.sum_till == None:
        filter_query = filter_query.where(
            payments_model.payment.c.sum <= filter.sum_till)
    if not filter.date_from == None:
        filter_query = filter_query.where(
            payments_model.payment.c.date >= filter.date_from)
    if not filter.date_till == None:
        filter_query = filter_query.where(
            payments_model.payment.c.date <= filter.date_till)

    results = await database.fetch_all(filter_query.order_by(payments_model.payment.c.id))

    return [dict(result._mapping) for result in results]


async def create_payment(payment: payments_schema.PaymentCreate):
    """Create new payment"""

    query = payments_model.payment.insert().values(fk_booking_id=payment.booking_id,
                                                   sum=payment.sum,
                                                   date=payment.date,
                                                   description=payment.description)
    payment_id = await database.execute(query)

    result = await check_is_paid(payment.booking_id)

    return {**payment.dict(), "id": payment_id}


async def check_is_paid(booking_id: int):
    """Check&Set if booking is paid"""

    results = await database.fetch_all(payments_model.payment.select().where(
        payments_model.payment.c.fk_booking_id == booking_id))
    payments_booking = [dict(result._mapping)['sum'] for result in results]
    sum_payment_bookings = sum(payments_booking)
    results = await database.fetch_one(bookings_model.booking.select().where(
        bookings_model.booking.c.id == booking_id))
    room_number = dict(results._mapping)['fk_room_number']
    results = await database.fetch_one(rooms_model.room.select().where(
        rooms_model.room.c.number == room_number))
    room_type = dict(results._mapping)['fk_room_types_id']
    results = await database.fetch_one(rooms_model.room_type.select().where(
        rooms_model.room_type.c.id == room_type))
    price = dict(results._mapping)['price']
    if sum_payment_bookings >= price:
        query = bookings_model.booking.update().values(is_paid=True).where(
            bookings_model.booking.c.id == booking_id)
    else:
        query = bookings_model.booking.update().values(is_paid=False).where(
            bookings_model.booking.c.id == booking_id)
    await database.execute(query)

    return sum_payment_bookings >= price


async def update_payment(payment_id, payment: payments_schema.PaymentCreate):
    """Update the payment"""

    query = payments_model.payment.select().where(
        payments_model.payment.c.id == payment_id)
    answer = await database.execute(query)
    if answer == payment_id:
        query = payments_model.payment.update().values(
            fk_booking_id=payment.booking_id,
            sum=payment.sum,
            date=payment.date,
            description=payment.description).where(
            payments_model.payment.c.id == payment_id)
        await database.execute(query)

        result = await check_is_paid(payment.booking_id)
        return {**payment.dict(), "id": payment_id}
    else:
        raise HTTPException(status_code=404, detail="Not found")


async def delete_payment(payment_id: int):
    """Delete payment by id"""

    query = payments_model.payment.select().where(
        payments_model.payment.c.id == payment_id)
    answer = await database.execute(query)
    if answer == payment_id:
        query = payments_model.payment.delete().where(
            payments_model.payment.c.id == payment_id)
        await database.execute(query)
        answer = "Success"
    else:
        answer = "Error"
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}