from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api

app = FastAPI()

# SUB APPS
# api
# frontend


@app.get("/")
def home():
    return "hapy api, what can we do ya for?"


app.mount("/api", api)
