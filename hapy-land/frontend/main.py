from logging import error
from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.sql.functions import current_date, current_user
from api.schemas import User as UserSchema
from sqlalchemy.orm import Session


from api.users import get_current_user2
from api import crud
from api.database import SessionLocal

frontend = FastAPI()

frontend.mount("/static", StaticFiles(directory="frontend/static"), name="static")


templates = Jinja2Templates(directory="frontend/templates")
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@frontend.get("/", response_class=HTMLResponse)
async def index(
    request: Request, current_user: UserSchema = Depends(get_current_user2)
):
    return templates.TemplateResponse(
        "index.html", {"request": request, "user": current_user}
    )


@frontend.get("/examples", response_class=HTMLResponse)
async def examples(
    request: Request,
    current_user: UserSchema = Depends(get_current_user2),
    db: Session = Depends(get_db),
):
    examples = crud.get_challenges(db)
    return templates.TemplateResponse(
        "examples.html",
        {"request": request, "user": current_user, "examples": examples},
    )


@frontend.get("/examples/{id}", response_class=HTMLResponse)
async def example(
    request: Request,
    id: str,
    current_user: UserSchema = Depends(get_current_user2),
    db: Session = Depends(get_db),
):
    challenge = crud.get_challenge_by_id(db, id)
    if challenge:
        return templates.TemplateResponse(
            "example.html",
            {
                "request": request,
                "id": id,
                "user": current_user,
                "challenge": challenge,
            },
        )
    return templates.TemplateResponse(
        "error.html", {"request": request, "error_code": 404, "user": current_user}
    )


@frontend.get("/bites", response_class=HTMLResponse)
async def bites(
    request: Request,
    current_user: UserSchema = Depends(get_current_user2),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    bites = crud.get_bites(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "bites.html",
        {"request": request, "id": id, "user": current_user, "bites": bites},
    )


@frontend.get("/bites/{id}", response_class=HTMLResponse)
async def bite(
    request: Request, id: str, current_user: UserSchema = Depends(get_current_user2)
):
    return templates.TemplateResponse(
        "bite.html", {"request": request, "id": id, "user": current_user}
    )


@frontend.get("/login", response_class=HTMLResponse)
async def login(
    request: Request, current_user: UserSchema = Depends(get_current_user2)
):
    return templates.TemplateResponse(
        "login.html", {"request": request, "user": current_user}
    )


@frontend.get("/logout")
async def logout(current_user: UserSchema = Depends(get_current_user2)):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not logged in")

    res = RedirectResponse(url=f"/?show_toast&msg=logout_success", status_code=303)

    res.set_cookie(key="hapyland_token", value="", expires=-70000)

    return res


@frontend.get("/register", response_class=HTMLResponse)
async def register(
    request: Request, current_user: UserSchema = Depends(get_current_user2)
):
    return templates.TemplateResponse(
        "register.html", {"request": request, "user": current_user}
    )


@frontend.get("/editor/{id}", response_class=HTMLResponse)
async def editor(
    request: Request, id: int, current_user: UserSchema = Depends(get_current_user2)
):
    return templates.TemplateResponse(
        "editor.html", {"request": request, "user": current_user}
    )


@frontend.get("/verify-token/{token}", response_class=HTMLResponse)
async def verify_token(request: Request, token):
    return templates.TemplateResponse(
        "verify_token.html", {"request": request, "token": token}
    )


@frontend.get("/admin/add_example")
def admin_add_examples(
    request: Request, current_user: UserSchema = Depends(get_current_user2)
):
    if current_user and current_user.is_superuser:
        return templates.TemplateResponse(
            "add_examples.html",
            {"request": request, "user": current_user},
        )
    raise HTTPException(status_code=401, detail="You do not have access!")
