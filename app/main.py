from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return "hapy api, what can we do ya for?"


app.mount("/api", api)
