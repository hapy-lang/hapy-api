from fastapi import FastAPI


backend = FastAPI()

@backend.get("/")
def index():
    return "Home"