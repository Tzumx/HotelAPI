"""Different crud-functions to work with requests."""

from fastapi import HTTPException

from db import database
from models import requests as requests_model
from schemas import requests as requests_schema


async def filter_requests(filter: requests_schema.RequestFilter,
                          offset: int = 0, limit: int = 100):
    """Get filter list of requests"""

    filter_query = requests_model.request.select()
    if not filter.booking_id == None:
        filter_query = filter_query.where(
            requests_model.request.c.fk_booking_id == filter.booking_id)
    if not filter.is_closed == None:
        filter_query = filter_query.where(
            requests_model.request.c.is_closed == filter.is_closed)
    if not filter.price_from == None:
        filter_query = filter_query.where(
            requests_model.request.c.price >= filter.price_from)
    if not filter.price_till == None:
        filter_query = filter_query.where(
            requests_model.request.c.price <= filter.price_till)
    if not filter.date_creation_from == None:
        filter_query = filter_query.where(
            requests_model.request.c.created_at >= filter.date_creation_from)
    if not filter.date_creation_till == None:
        filter_query = filter_query.where(
            requests_model.request.c.created_at <= filter.date_creation_till)

    results = await database.fetch_all(filter_query.order_by(requests_model.request.c.id))

    return [dict(result._mapping) for result in results]


async def create_request(request: requests_schema.RequestCreate):
    """Create new request"""

    query = requests_model.request.insert().values(fk_booking_id=request.booking_id,
                                                   price=request.price,
                                                   description=request.description)
    request_id = await database.execute(query)
    query = requests_model.request.select().where(
        requests_model.request.c.id == request_id)
    results = await database.fetch_one(query)
    return dict(results._mapping)


async def update_request(request_id, request: requests_schema.RequestUpdate):
    """Update the request"""

    query = requests_model.request.select().where(
        requests_model.request.c.id == request_id)
    stored_data = await database.fetch_one(query)
    if stored_data != None:
        stored_data = dict(stored_data._mapping)
        update_data = request.dict(exclude_unset=True)
        stored_data.update(update_data)
        query = requests_model.request.update().values(**stored_data).where(
            requests_model.request.c.id == request_id)
        await database.execute(query)
        return {**stored_data, "id": request_id}
    else:
        raise HTTPException(status_code=404, detail="Not found")


async def delete_request(request_id: int):
    """Delete request by id"""

    query = requests_model.request.select().where(
        requests_model.request.c.id == request_id)
    answer = await database.execute(query)
    if answer == request_id:
        query = requests_model.request.delete().where(
            requests_model.request.c.id == request_id)
        await database.execute(query)
        answer = "Success"
    else:
        answer = "Error"
        raise HTTPException(status_code=404, detail="Not found")
    return {"result": answer}
