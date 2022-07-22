from fastapi import FastAPI
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


if __name__ == '__main__':
    uvicorn.run("__main__:app", host="0.0.0.0", port=8001,
                reload=True, workers=2, debug=True)
