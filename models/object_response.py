from pydantic import BaseModel

class ObjectData(BaseModel):
    year: int
    price: float

class ObjectResponse(BaseModel):
    id: str
    name: str
    data: ObjectData