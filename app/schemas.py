from pydantic import BaseModel, EmailStr, Field


class UserReg(BaseModel):
    name: str = Field(max_length=50, min_length=5)
    email: EmailStr
    password: str = Field(min_length=8)


class UserAuthReg(BaseModel):
    login: str = Field(min_length=5)
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    token: str
    id: str
