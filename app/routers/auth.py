from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from time import time_ns
from database import get_db
from func import badresponse
import uuid
import crud
import schemas
import models
import os
import re
import jwt


router = APIRouter(prefix="/api/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def getkey() -> str:
    return os.getenv(
        "RANDOM_SECRET",
        "4tESqoGKgye6KYAO7lwdzs3VjXRd8TSE9iKqwBlJBEs0rS652RGzH9EIe8IhF5aqo3zgmjbOX2vyIrlAozF8CJrSyg7LcQyMDgbrxGsizQc2JRp07K7jJJ2aWXRPjoPN",
    )


def gen_jwt(obj: str, include_time: bool) -> str:
    if include_time:
        return jwt.encode({"data": obj, "time": time_ns()}, getkey(), algorithm="HS256")
    return jwt.encode({"data": obj}, getkey(), algorithm="HS256")


def dec_jwt(obj: str) -> str:
    return jwt.decode(obj, getkey(), algorithms="HS256")


@router.post("/sign-up", response_model=schemas.UserResponse)
async def sign_up(user: schemas.UserReg, db: Session = Depends(get_db)):
    pwd = user.password
    if (
        not re.search(r"\d", pwd)
        or not re.search(r"[a-z]", pwd)
        or not re.search(r"[A-Z]", pwd)
        or not re.search(r"[!@#$%^&*()\-_=+[\]{};:'\",.<>?/]", pwd)
    ):
        return badresponse("Easy password.")
    else:
        pwd_hash = pwd_context.hash(pwd)
        token = gen_jwt(user.email, True)
        user_id = str(uuid.uuid4())
        us = crud.createUser(db, user_id, user.name, user.email, pwd_hash, token)
        if not us:
            return JSONResponse(
                status_code=409,
                content={
                    "status": "error",
                    "message": "Такой email уже зарегистрирован.",
                },
            )
    return schemas.UserResponse(token=token, id=user_id)


@router.post("/sign-in", response_model=schemas.UserResponse)
async def sign_in(user: schemas.UserAuthReg, db: Session = Depends(get_db)):
    if "@" in user.login:
        usr_db = crud.get(db, models.User, models.User.email, user.login)
        if usr_db:
            if pwd_context.verify(user.password, usr_db.password_hash):
                token = gen_jwt(user.login, True)
                usr_db.token = token
                crud.updtoken(db, models.User, usr_db.id, token)
                return schemas.UserResponse(token=token, id=usr_db.id)
            else:
                return JSONResponse(
                    content={"message": "Error. Invalid password."}, status_code=403
                )
        else:
            return JSONResponse(
                content={"message": "Error. User not found."}, status_code=404
            )
    else:
        usr_db = crud.getall(db, models.User, models.User.name, user.login)
        if usr_db:
            for x in usr_db:
                if pwd_context.verify(user.password, x.password_hash):
                    token = gen_jwt(x.email, True)
                    x.token = token
                    crud.updtoken(db, models.User, x.id, token)
                    return schemas.UserResponse(token=token, id=x.id)
            return JSONResponse(
                content={"message": "Error. Invalid password."}, status_code=403
            )
        else:
            return JSONResponse(
                content={"message": "Error. User not found."}, status_code=404
            )
