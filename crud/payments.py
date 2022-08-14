"""Different crud-functions to work with payments."""

from fastapi import HTTPException

from crud import bookings as bookings_crud
from db import database
from models import bookings as bookings_model
from models import payments as payments_model
from models import rooms as rooms_model
from schemas import payments as payments_schema


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
    results = await bookings_crud.get_booking_sum(booking_id)
    price = results['sum']
    if sum_payment_bookings >= price:
        query = bookings_model.booking.update().values(is_paid=True).where(
            bookings_model.booking.c.id == booking_id)
    else:
        query = bookings_model.booking.update().values(is_paid=False).where(
            bookings_model.booking.c.id == booking_id)
    await database.execute(query)

    return sum_payment_bookings >= price


async def update_payment(payment_id, payment: payments_schema.PaymentUpdate):
    """Update the payment"""

    query = payments_model.payment.select().where(
        payments_model.payment.c.id == payment_id)
    stored_data = await database.fetch_one(query)
    if stored_data != None:
        stored_data = dict(stored_data._mapping)
        update_data = payment.dict(exclude_unset=True)
        stored_data.update(update_data)
        query = payments_model.payment.update().values(**stored_data).where(
            payments_model.payment.c.id == payment_id)
        await database.execute(query)

        result = await check_is_paid(stored_data['fk_booking_id'])
        return {**stored_data, "id": payment_id}
    else:
        raise HTTPException(status_code=404, detail="Not found")


async def delete_payment(payment_id: int):
    """Delete payment by id"""

    query = payments_model.payment.select().where(
        payments_model.payment.c.id == payment_id)
    stored_data = await database.fetch_one(query)
    if stored_data != None:
        query = payments_model.payment.delete().where(
            payments_model.payment.c.id == payment_id)
        await database.execute(query)
        result = await check_is_paid(stored_data['fk_booking_id'])
        answer = "Success"
    else:
        answer = "Error"
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}
