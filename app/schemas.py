from typing import Optional, List, Dict, Union, Any
from pydantic import BaseModel, EmailStr, Field


class UserReg(BaseModel):
    name: str = Field(max_length=100, min_length=5)
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    token: str
    id: str

class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)