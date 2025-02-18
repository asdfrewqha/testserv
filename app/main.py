import os
import uvicorn
from func import badresponse
from routers import auth
from database import Base, engine
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любого источника
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return badresponse("Invalid request.")


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/sign_up")
async def signup_ep(request: Request):
    return templates.TemplateResponse("sign_up.html", {"request": request})


@app.get("/sign_in")
async def signin_ep(request: Request):
    return templates.TemplateResponse("sign_in.html", {"request": request})

@app.get("/test")
async def test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

if __name__ == "__main__":
    server_address = os.getenv("SERVER_ADDRESS", "0.0.0.0:4000")
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))
