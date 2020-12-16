from pydantic import BaseModel

class UserIn(BaseModel):
    user: str
    password: str


class UserOut(BaseModel):
    name: str
    total: int