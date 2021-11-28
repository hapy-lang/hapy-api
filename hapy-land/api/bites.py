from typing import List
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from importlib.metadata import version

# Local  imports aka imports from the lib.
from .database import SessionLocal
from . import schemas, crud
from .schemas import Response
from .users import get_current_user, oauth2_scheme

router = APIRouter(
    prefix="/bites",
    tags=["bites"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# routes
# create user
# get user


@router.get("/", response_model=Response[List[schemas.Bite]])
async def read_bites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bites = crud.get_bites(db, skip=skip, limit=limit)
    return Response[List[schemas.Bite]](data=bites, status="success", message="Bites fetched successfully!")

@router.get("/b/{bite_id}", response_model=Response[schemas.Bite])
async def fetch_bite(bite_id: int, db: Session = Depends(get_db)):
    bite = crud.get_bite_by_id(db, bite_id=bite_id)
    if bite is None:
        raise HTTPException(status_code=404, detail="Bite not found")
    return Response[schemas.Bite](data=bite, status="success", message="Bites fetched successfully!")

@router.post("/", response_model=Response[schemas.Bite])
def upload_bite(bite: schemas.BiteCreate, db: Session = Depends(get_db), token = Depends(oauth2_scheme), current_user: schemas.User = Depends(get_current_user)):

    # TODO: change this to Hapy_version
    # get installed Hapy version o

    created_bite = crud.create_bite(db=db, item=bite, submitter_id=current_user.id, hapy_v=version('Hapy'))

    if created_bite is None:
        raise HTTPException(status_code=400, detail="Bite not created!")

    return Response[schemas.Bite](data=created_bite, status="success", message="Bite uploaded successfully!")