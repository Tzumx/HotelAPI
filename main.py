from fastapi import FastAPI
import uvicorn


# Initialize the app
app = FastAPI()


if __name__ == '__main__':
    uvicorn.run("__main__:app", host="0.0.0.0", port=8001,
                reload=True, workers=2, debug=True)
