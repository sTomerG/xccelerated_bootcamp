from pydantic import BaseModel



class BarModel(BaseModel):
    whatever: int


class FooBarModel(BaseModel):
    banana: float
    foo: str


dict = {}
dict['test'] = FooBarModel(banana=3.14, foo="hello")

print(dict['test'])
"""
{
    'banana': 3.14,
    'foo': 'hello',
    'bar': BarModel(
        whatever=123,
    ),
}
"""
for name, value in m:
    print(f"{name}: {value}")
    # > banana: 3.14
    # > foo: hello
    # > bar: whatever=123
