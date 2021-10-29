from fastapi import FastAPI
from api.main import api
from frontend.main import frontend


app = FastAPI()

# SUB APPS
# api
# frontend

@app.get("/home")
def home():
    return "Thank you Jesus!"

app.mount("/api", api)
app.mount("/", frontend)
