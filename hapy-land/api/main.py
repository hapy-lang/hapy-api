from fastapi import FastAPI


api = FastAPI()

@api.get("/")
def index():
    return {"data": "Index"}