from datetime import datetime
from fastapi import (
    FastAPI,
    status,
    Depends,
    HTTPException,
    Response,
    File,
    UploadFile,
    Form,
)
from sqlalchemy.orm import Session
from typing import Optional

# Hapy imports
from hapy.transpiler import transpile
from hapy.exector import run as run_python


# Local  imports aka imports from the lib.
from .database import SessionLocal, engine
from . import models
from .schemas import Request, User, RequestResponse
from .users import router as users_router
from .bites import router as bites_router
from .challenges import router as challenges_router
from sqlalchemy_utils import create_database, database_exists


api = FastAPI()

# Create
# Retrieve
# Update
# Delete CRUD

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if not database_exists(engine.url):
    create_database(engine.url)

models.Base.metadata.create_all(engine)

api.include_router(users_router)
api.include_router(bites_router)
api.include_router(challenges_router)

# TODO: maybe should be moved...
def execute(req):
    translated = None
    python_result = None
    try:
        if req.code:
            code_in_python = transpile(req.code)
            result = "No output"
            error = ""
            # if compile only is true
            if not req.compile_only:
                result = run_python(code_in_python, return_output=True, cloud=True)
                python_result = result[1] if result[1] else result[0]
                error = result[0]
            translated = code_in_python

            return {
                "data": {
                    "python_result": python_result,
                    "python_source": translated,
                    "error": error,
                },
                "status": "success" if (python_result or translated) else "error",
                "message": "Hapy output"
                if not error
                else "Error while compiling Hapy!",
            }
        return {
            "data": {"python_result": None, "python_source": None},
            "status": "error",
            "message": "Invalid code/ or file",
        }
    except Exception as e:
        return {
            "data": {"error": str(e)},
            "status": "error",
            "message": "Error while compiling Hapy",
        }


@api.post("/run", response_model=RequestResponse, status_code=status.HTTP_200_OK)
def run(item: Request):
    """Execute code, transpile code, execute and transpile"""
    if item.code:
        return execute(req=item)
    else:
        return {
            "data": {"python_result": None, "python_source": None},
            "status": "error",
            "message": "Invalid code/ or file",
        }


@api.post("/run_file/")
async def create_upload_file(file: UploadFile = File(...), option: str = Form(...)):

    content = await file.read()
    content = content.decode("utf-8")
    return execute(content, option=option)
