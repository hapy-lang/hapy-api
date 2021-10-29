from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

backend = FastAPI()

backend.mount("/static", StaticFiles(directory="backend/static"), name="static")


templates = Jinja2Templates(directory="backend/templates")

@backend.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@backend.get("/examples", response_class=HTMLResponse)
def examples(request: Request):
    return templates.TemplateResponse("examples.html", {"request": request})

@backend.get("/examples/{id}", response_class=HTMLResponse)
def example(request: Request, id: str):
    return templates.TemplateResponse("example.html", {"request": request, "id": id})

@backend.get("/bites", response_class=HTMLResponse)
def bites(request: Request):
    return templates.TemplateResponse("bites.html", {"request": request, "id": id})

@backend.get("/bites/{id}", response_class=HTMLResponse)
def bite(request: Request, id: str):
    return templates.TemplateResponse("bite.html", {"request": request, "id": id})



