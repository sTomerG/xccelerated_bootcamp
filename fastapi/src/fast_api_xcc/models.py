from pydantic import BaseModel, StrictInt, StrictStr


class Person(BaseModel):
    name: StrictStr
    age: StrictInt
