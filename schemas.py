from typing import Optional

from pydantic import BaseModel, EmailStr


class Student(BaseModel):
    name: str
    className: str
    rollNumber: int
    image: str

    class Config:
        orm_mode = True


class GetStudent(Student):
    uid: str

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr


class UserLogin(User):
    password: str


class GetUser(User):
    uid: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uid: Optional[str] = None
