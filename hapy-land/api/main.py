from fastapi import FastAPI
from hapy.transpiler import transpile
from hapy.exector import run as run_python

from .models import Request


api = FastAPI()

# Create
# Retrieve
# Update
# Delete CRUD


@api.get("/")
def index():
    return {"data": "Index"}


@api.post("/run")
def run(item: Request):
    """Execute code, transpile code, execute and transpile"""
    if item.code != None:
        translated = transpile(item.code)
        if item.translate and not item.execute_only:
            """This returns python source code and a result from python_source execution"""
            executed = run_python(translated, cloud=False, return_output=True)
            # executed returns a tuple of (error, result)
            python_result = executed[1] if executed[0] == "" else executed[0]
            return {
                "data": {"python_result": python_result, "python_source": translated},
                "status": "success",
                "message": "Python equivalence of Hapy Code + Result of Hapy execution",
            }
        elif item.execute_only:
            # This checks if the user wants just a python_source
            return {
                "data": {"python_source": translated},
                "status": "success",
                "message": "Python equivalence of Hapy code",
            }
        else:
            return {
                "data": None,
                "status": "error",
                "message": "translate and execute_only cannot be both false",
            }
