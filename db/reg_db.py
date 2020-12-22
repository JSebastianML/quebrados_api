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

def find_one_register(identificador: int):
    for reg in database_registers:
        if identificador == reg.id_register:
            return reg

def find_register(user: str):
    find = []
    for reg in database_registers:
        if user == reg.user:
            find.append(reg)
    return find   

def delete_register(identificador: int):
    for reg in database_registers:
        if (identificador == reg.id_register):
            database_registers.pop(database_registers.index(reg)) 

def delete_user_registers(user: str):
    for reg in database_registers:
        if (user == reg.user):
            database_registers.pop(database_registers.index(reg)) 

def check_register(user:str, id_reg: int):
    for reg in database_registers:
        if (user == reg.user and id_reg == reg.id_register):
            return True
    return False 

