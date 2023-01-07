from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import text

from database import Base


class User(Base):
    __tablename__ = "users"
    uid = Column(
        String,
        nullable=True,
        primary_key=True,
        server_default=text("REPLACE(gen_random_uuid()::text,'-','')"),
    )
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    class Config:
        orm_mode = True


class Student(Base):
    __tablename__ = "students"
    uid = Column(
        String,
        primary_key=True,
        nullable=True,
        index=True,
        server_default=text("REPLACE(gen_random_uuid()::text,'-','')"),
    )
    name = Column(String, nullable=False)
    className = Column(String, nullable=False)
    rollNumber = Column(Integer, nullable=False, unique=True)

    class Config:
        orm_mode = True


class TokenBlackList(Base):
    __tablename__ = "tokenblacklist"
    _id = Column(Integer, primary_key=True, nullable=True)
    token = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)

    class Config:
        orm_mode = True
