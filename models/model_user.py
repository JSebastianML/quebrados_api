from pydantic import BaseModel

class UserIn(BaseModel):
    user: str
    password: str

class CreateUserIn(BaseModel):
    user: str
    name: str
    password: str

class UserOut(BaseModel):
    name: str
    total: int