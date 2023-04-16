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
    challenge_id: int

    class Config:
        orm_mode = True


class RequestResponse(BaseModel):
    data: Dict
    status: str
    message: str