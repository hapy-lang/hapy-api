from importlib.metadata import version
from typing import List
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

# Local  imports aka imports from the lib.
from .database import SessionLocal
from . import schemas, crud
from .schemas import Response
from .users import get_current_user, oauth2_scheme

router = APIRouter(
    prefix="/challenges",
    tags=["challenges"],
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


@router.get("/", response_model=Response[List[schemas.Challenge]])
async def read_challenges(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    challenges = crud.get_challenges(db, skip=skip, limit=limit)
    print(challenges)
    return Response[List[schemas.Challenge]](
        data=challenges, status="success", message="Challenges fetched successfully!"
    )


@router.get("/c/{challenge_id}", response_model=Response[schemas.Challenge])
async def read_challenge(challenge_id: int, db: Session = Depends(get_db)):
    challenge = crud.get_challenge_by_id(db, challenge_id=challenge_id)
    if challenge is None:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return Response[schemas.Challenge](
        data=challenge, status="success", message="Challenge fetched successfully!"
    )


@router.post("/", response_model=Response[schemas.Challenge])
def create_challenge(
    challenge: schemas.ChallengeCreate,
    db: Session = Depends(get_db),
    token=Depends(oauth2_scheme),
):
    if challenge.description is None or challenge.title is None:
        raise HTTPException(status_code=400, detail="Bad request!")
    created_challenge = crud.create_challenge(db=db, item=challenge)
    if created_challenge is None:
        raise HTTPException(status_code=400, detail="Challenge not created!")
    return Response[schemas.Challenge](
        data=created_challenge,
        status="success",
        message="Challenge uploaded successfully!",
    )


@router.post("/{challenge_id}/solution", response_model=Response[schemas.Solution])
def add_solution_to_challenge(
    challenge_id: int,
    solution: schemas.SolutionCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):

    solution_by_user = crud.get_solution_by_user(
        db=db, user_id=current_user.id, challenge_id=challenge_id
    )
    challenge = crud.get_challenge_by_id(db=db, challenge_id=challenge_id)

    if challenge is None:
        raise HTTPException(status_code=400, detail="Challenge not created!")
    if solution_by_user:
        raise HTTPException(
            status_code=400, detail="You have already created a solution!"
        )

    created_solution = crud.create_solution(
        db=db,
        challenge_id=challenge_id,
        item=solution,
        submitter_id=current_user.id,
        hapy_v=version("Hapy"),
    )
    if created_solution is None:
        raise HTTPException(status_code=400, detail="Solution not added!")

    return Response[schemas.Solution](
        data=created_solution, status="success", message="Solution added successfully!"
    )
