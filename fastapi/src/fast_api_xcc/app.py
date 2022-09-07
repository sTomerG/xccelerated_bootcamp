from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from redis import Redis

from fast_api_xcc.models import Person

red: Redis = Redis(decode_responses=True)
app: FastAPI = FastAPI()
red.set("persons", )


@app.get("/")
def index():
    return {"Hello from the index"}


@app.post("/names/", status_code=201)
def post_names(person: Person):
    dictio = {person.name: person}
    red.hset('persons', mapping=dict(person))
    return JSONResponse(f"Added {person.name} to database")


@app.get("/names/", status_code=200)
def get_all_names():
    return JSONResponse(list(red.hget()))


@app.get("/names/{name}", status_code=200)
def get_name(name: str):
    try:
        print(dict(persons[name]))
    except KeyError:
        raise HTTPException(404, f"'{name}' not known in database")

    return JSONResponse(dict(persons[name]))
