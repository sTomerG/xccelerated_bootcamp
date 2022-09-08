import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from redis import Redis

from fastapi_xcc.models import Person

red: Redis = Redis(
    host="docker.for.mac.localhost", port=6379, decode_responses=True
)
app: FastAPI = FastAPI()


@app.get("/")
def index():
    return {"Hello from the index!"}


@app.post("/names/", status_code=201)
def post_names(person: Person):
    red.hset("persons", person.name, person.json())
    return JSONResponse(f"Added {person.name} to database")


@app.get("/names/", status_code=200)
def get_all_names():
    return JSONResponse(list(red.hgetall("persons")))


@app.get("/names/{name}", status_code=200)
def get_name(name: str):
    try:
        person = red.hget("persons", name)
    except KeyError:
        raise HTTPException(404, f"'{name}' not known in database")

    return JSONResponse(json.loads(person))
