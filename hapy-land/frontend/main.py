from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

frontend = FastAPI()

frontend.mount("/static", StaticFiles(directory="frontend/static"), name="static")


templates = Jinja2Templates(directory="frontend/templates")

@frontend.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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


