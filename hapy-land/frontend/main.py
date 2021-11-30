from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.schemas import User as UserSchema

from api.users import get_current_user2

frontend = FastAPI()

frontend.mount("/static", StaticFiles(directory="frontend/static"), name="static")


templates = Jinja2Templates(directory="frontend/templates")


@frontend.get("/", response_class=HTMLResponse)
def index(request: Request, current_user: UserSchema = Depends(get_current_user2)):
    return templates.TemplateResponse(
        "index.html", {"request": request, "user": current_user}
    )


@frontend.get("/examples", response_class=HTMLResponse)
def examples(request: Request):
    return templates.TemplateResponse("examples.html", {"request": request})


@frontend.get("/examples/{id}", response_class=HTMLResponse)
def example(request: Request, id: str):
    return templates.TemplateResponse("example.html", {"request": request, "id": id})


@frontend.get("/bites", response_class=HTMLResponse)
def bites(request: Request):
    return templates.TemplateResponse("bites.html", {"request": request, "id": id})


@frontend.get("/bites/{id}", response_class=HTMLResponse)
def bite(request: Request, id: str):
    return templates.TemplateResponse("bite.html", {"request": request, "id": id})


@frontend.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@frontend.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@frontend.get("/editor", response_class=HTMLResponse)
def editor(request: Request):
    return templates.TemplateResponse("editor.html", {"request": request})


@frontend.post("/auth/login")
def login_user():
    return {"data": "Find me in the main.py of frontend"}


@frontend.get("/verify-token/{token}", response_class=HTMLResponse)
async def verify_token(request: Request, token):
    return templates.TemplateResponse(
        "verify_token.html", {"request": request, "token": token}
    )


@frontend.get("/admin/add_example")
def admin_add_examples(
    request: Request, current_user: UserSchema = Depends(get_current_user2)
):
    if current_user.is_superuser:
        return templates.TemplateResponse(
            "add_examples.html",
            {"request": request, "user": current_user},
        )
    raise HTTPException(status_code=401, detail="You do not have access!")
