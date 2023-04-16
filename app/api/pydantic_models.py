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
