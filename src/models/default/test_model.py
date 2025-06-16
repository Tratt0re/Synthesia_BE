from pydantic import BaseModel


class TestModel(BaseModel):
    name: str
    value: int | None = None