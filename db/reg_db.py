from pydantic import BaseModel
from datetime import date

class bd_register (BaseModel):
    id_register : int = 0
    user : str
    category : str
    concept : str
    value : int
    fecha : date = date.today()

database_registers = []

identifier = {"id":0}

def save_register(register: bd_register):
    identifier["id"] += 1
    register.id_register = identifier ["id"]
    #register.date = date.today()
    database_registers.append(register)
    return register

def find_register(user: str):
    find = []
    for reg in database_registers:
        if user == reg.user:
            find.append(reg)
    return find   



