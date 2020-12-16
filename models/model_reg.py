from pydantic import BaseModel
from datetime import date

class RegisterIn(BaseModel):
    user : str
    category : str
    concept : str
    value : int

class RegisterOut(BaseModel):
    id_register : int
    user : str
    category : str
    concept : str
    value : int
    fecha : date
    total: int
    