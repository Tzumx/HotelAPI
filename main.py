from asyncpg.exceptions import ForeignKeyViolationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
import uvicorn
from db import database
from routers import rooms

# Initialize the app
app = FastAPI()

# Link all URLs
app.include_router(rooms.router)


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
