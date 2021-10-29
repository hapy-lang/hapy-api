from pydantic import BaseModel
from typing import Optional


class Request(BaseModel):
    code: str
    translate: Optional[bool]
    save: Optional[bool]
    execute_only: Optional[bool] = False
