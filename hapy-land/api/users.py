from fastapi import (
    APIRouter,
    Depends,
    Cookie,
    status,
    HTTPException,
    Response as Response_class,
)
from fastapi.param_functions import Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

# Local  imports aka imports from the lib.
from .database import SessionLocal
from .models import User as UserModel
from . import schemas, crud
from .schemas import User as UserSchema, Response

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

router = APIRouter(
    prefix="/users",
    tags=["users"],
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


@router.get("/", response_model=Response[List[schemas.User]])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token=Depends(oauth2_scheme),
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return Response[List[schemas.User]](
        data=users, status="success", message="Users fetched successfully!"
    )


@router.get("/u/{user_id}", response_model=Response[schemas.User])
async def read_user(
    user_id: int, db: Session = Depends(get_db), token=Depends(oauth2_scheme)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response[schemas.User](
        data=db_user, status="success", message="User fetched successfully!"
    )


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=Response[schemas.User],
)
def register_user_using_form(
    form: Optional[bool] = False,
    username: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    confirm_password: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    if confirm_password != password:
        raise HTTPException(status_code=400)
    new_user = {"username": username, "email": email, "password": password}

    """A Post request to send new user data and write it to a data store."""

    created_at = datetime.now()
    updated_at = datetime.now()
    # Hash the password

    register = UserModel(**new_user, created_at=created_at, updated_at=updated_at)

    # Verify That this user does not exist
    db_user = (
        db.query(UserModel).filter(UserModel.username == new_user["username"]).count()
    )
    if db_user > 0:
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        db.add(register)
        db.commit()
        db.refresh(register)
    except Exception as e:
        print("ERROR while adding user => ", e)
        raise HTTPException(status_code=400, detail="Something went wrong!")
    # return register
    # or

    # TODO: if there's an error while making this user, revert db operation :)
    if form:
        return RedirectResponse(url="/login?show_toast&msg=registered_successfully", status_code=303)
    return Response[schemas.User](
        data=register, status="success", message="User created successfully!"
    )


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version

    # NOTE: for now the username is the user's token
    db = SessionLocal()

    user = crud.get_user_by_username(db, username=token)
    return user


# this token kini means it expects the "Bearer {token}" Authorization
# header as part of the request...
# thank you Jesus!
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_cookie(hapyland_token: Optional[str] = Cookie(None)):
    return hapyland_token


async def get_current_user2(token: str = Depends(get_cookie)):
    user = fake_decode_token(token)
    return user


@router.post("/token")
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # hashed_password = fake_hash_password(form_data.password)
    if not form_data.password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # hashed_password = fake_hash_password(form_data.password)
    if not form_data.password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    res = RedirectResponse(
        url=f"/verify-token/{user.username}?type=bearer", status_code=303
    )

    res.set_cookie(key="hapyland_token", value=user.username)

    return res

@router.get("/me", response_model=Response[schemas.User])
async def read_users_me(current_user: UserSchema = Depends(get_current_user)):
    return Response[schemas.User](
        data=current_user, status="success", message="User fetched successfully!"
    )
