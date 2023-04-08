from fastapi import FastAPI
from api.main import api


app = FastAPI()

# SUB APPS
# api
# frontend


@app.get("/home")
def home():
    return "Thank you Jesus!"


app.mount("/api", api)
