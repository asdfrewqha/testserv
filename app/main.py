import os
import uvicorn
from func import badresponse
from routers import auth
from database import Base, engine
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return badresponse()


@app.get("/")
async def main():
    return JSONResponse(
        content={"message": "Server is running"},
        status_code=200)


if __name__ == "__main__":
    server_address = os.getenv("SERVER_ADDRESS", "0.0.0.0:4000")
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))
