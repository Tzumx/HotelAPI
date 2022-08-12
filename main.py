import uvicorn
from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from db import database
from routers import bookings, guests, payments, requests, rooms, users

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "roomtypes",
        "description": "Roomtypes (with characteristics like price and features) is basis for rooms.",
    },
    {
        "name": "rooms",
        "description": "Rooms with characteristics based on their type.",
    },
    {
        "name": "guests",
        "description": "Guests who can make a bookings.",
    },
    {
        "name": "bookings",
        "description": "Each booking connected with guest and room. Checkbox 'is_paid' calculate automatically based on costs and paymnets.",
    },
    {
        "name": "requests",
        "description": "Guest can make request. It can cost money (included in total booking price).",
    },
    {
        "name": "payments",
        "description": "Payments from guests. Based on them calculate if booking is paid.",
    },

]

# Initialize the app
app = FastAPI(title="HotelAPI", openapi_tags=tags_metadata, version="1.0.0",)


# Link all URLs
app.include_router(bookings.router)
app.include_router(guests.router)
app.include_router(payments.router)
app.include_router(requests.router)
app.include_router(rooms.router)
app.include_router(users.router)


@app.on_event('startup')
async def startup() -> None:
    await database.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    await database.disconnect()


@app.exception_handler(ForeignKeyViolationError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


if __name__ == '__main__':
    uvicorn.run("__main__:app", host="0.0.0.0", port=8001,
                reload=True, workers=2, debug=True)
