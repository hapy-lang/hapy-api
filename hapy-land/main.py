from fastapi import FastAPI
from api.main import api 
from backend.main import backend 


app = FastAPI()

# SUB APPS
# api
# backend

@app.get("/home")
def home():
    return "Thank you Jesus!"

app.mount("/api", api)
app.mount("/", backend)
