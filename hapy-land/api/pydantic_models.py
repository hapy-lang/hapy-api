from datetime import datetime
from fastapi import UploadFile, File
from pydantic import BaseModel
from typing import Optional, Dict

# Pydantic models
class Request(BaseModel):
    code: str
    option: str
    save: bool = False

    class Config:
        orm_mode = True


class RequestResponse(BaseModel):
    data: Dict
    status: str
    message: str


class User(BaseModel):
    username: str = "NewUser"
    password: str
    timestamp: datetime = datetime.now()
    email: str

    class Config:
        orm_mode = True
