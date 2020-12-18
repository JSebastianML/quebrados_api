from pydantic import BaseModel 
from typing import Dict

class db_user (BaseModel):
    user : str
    name : str
    password : str
    total : int

database_users = Dict [str, db_user]

database_users = {
    "laura53": db_user(**{"user":"laura53",
                        "name":"Laura Marcela Joya",  
                        "password":"march543",
                        "total":6000000}),
    "sebastian92": db_user(**{"user":"sebastian92",
                        "name":"Sebastian Moreno",  
                        "password":"1",
                        "total":3500000}),
    "carlos24": db_user(**{"user":"carlos24",
                        "name":"Carlos Monsalve",  
                        "password":"llanerisimo",
                        "total":7000000}),
    "ivan10": db_user(**{"user":"ivan10",
                        "name":"Ivan Daniel Ortiz",
                        "password":"spiderman",
                        "total":4500000}),
    "krls82": db_user(**{"user":"krls82",
                        "name":"Carlos Cortes Sanchez",  
                        "password":"2011",
                        "total":3000000})
}

#database_users.keys() --> lista de las llaves del diccionari de arriba
def get_user(user: str):
    if user in database_users.keys():
        return database_users[user]
    else:
        return None

def update_user(user_db: db_user):
    database_users[user_db.user] = user_db
    return user_db

def create_user_indb(newUser: db_user):
    database_users[newUser.user] = newUser
