from datetime import date, datetime
from fastapi import UploadFile, File, Form
from pydantic import BaseModel, validator, ValidationError
from typing import Any, List, Optional, Dict, Generic, TypeVar, Optional
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class Response(GenericModel, Generic[DataT]):
    status: str
    message: str
    data: Optional[DataT]
    error: Optional[Any]

    @validator("error", always=True)
    def check_consistency(cls, v, values):
        if v is not None and values["data"] is not None:
            raise ValueError("must not provide both data and error")
        if v is None and values.get("data") is None:
            raise ValueError("must provide data or error")
        return v


# Pydantic models
class Request(BaseModel):
    code: str
    option: str
    compile_only: bool = False
    save: bool = False

    class Config:
        orm_mode = True


class RequestResponse(BaseModel):
    data: Dict
    status: str
    message: str


# Bite stuff
class BiteBase(BaseModel):
    title: str
    code: str
    description: str


class BiteCreate(BiteBase):
    pass


class Bite(BiteBase):
    id: int
    slug: str
    submitter_id: int
    created_at: datetime
    updated_at: datetime
    type: str
    downloads: int
    stars: int
    version: int
    hapy_version: str

    class Config:
        orm_mode = True


# User stuff
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime
    email: str
    is_superuser: bool
    bites: List[Bite] = []
    is_active: bool

    class Config:
        orm_mode = True


class SolutionCreate(BiteCreate):
    pass


class Solution(Bite):
    challenge_id: int

    class Config:
        orm_mode = True


# Challenge stuff
class ChallengeBase(BaseModel):
    title: str
    description: str


class ChallengeCreate(ChallengeBase):
    pass


class Challenge(ChallengeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    solutions: List[Solution] = []

    class Config:
        orm_mode = True
