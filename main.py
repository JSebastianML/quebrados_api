from models.model_reg import RegisterIn, RegisterOut
from models.model_user import UserIn, UserOut, CreateUser
from db.users_db import db_user
from db.users_db import get_user, update_user, create_user_indb
from db.reg_db import bd_register
from db.reg_db import save_register, find_register
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

quebrados_app = FastAPI()

origins = [
    "http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
    "http://localhost", "http://localhost:8080", "https://quebrados-app12.herokuapp.com",
]

quebrados_app.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@quebrados_app.post("/register/create")
async def reg_create(register: RegisterIn):

    user_exist = get_user(register.user)

    if user_exist == None:
        raise HTTPException(status_code=404, detail="El usuario no está registrado")

    if register.category == "ingreso":
        user_exist.total = user_exist.total + register.value
    elif register.category == "egreso":
        user_exist.total = user_exist.total - register.value
    else:
        raise HTTPException(status_code=400, detail="Tipo de registro no válido")

    update_user(user_exist)

    new_register = bd_register(**register.dict())
    new_register = save_register(new_register)
    register_to_show = RegisterOut(**new_register.dict(), total = user_exist.total)

    return register_to_show, {"mensaje": "¡Registro exitoso!"}

@quebrados_app.get("/register/find/{user}")
async def reg_find(user : str):

    user_exists = get_user(user)

    if user_exists==None:
        raise HTTPException(status_code=404, detail="El usuario no está registrado")

    match_list = find_register(user_exists.user)
    
    if len(match_list) > 0:
        return match_list
    else:
        return {"mensaje":"El usuario aún no tiene registros"} 

@quebrados_app.post("/user/login")
async def autentication(datos_entrada: UserIn):
    usuario_en_db = get_user(datos_entrada.user)
    
    if (usuario_en_db==None):
        return {"respuesta": False}
    if (usuario_en_db.password==datos_entrada.password):
        return {"respuesta": True}
    else:
        return {"respuesta": False}

@quebrados_app.get("/user/dashboard/{user}")
async def get_total(user: str):
    usuario = get_user(user)
    usuario= UserOut(**usuario.dict())
    return usuario

@quebrados_app.post("/user/register")
async def create_user(datosRegistro: CreateUser):
    user_exists = get_user(datosRegistro.name)
    if (user_exists!=None):
        return {"respuesta": "Lo sentimos, el nombre de usuario ya está en uso"}
    else:
        datosRegistro=db_user(**datosRegistro.dict(), total=0)
        create_user_indb(datosRegistro)
        return {"respuesta": "El usuario se registró correctamente. Por favor ingresa a continuación con tu nuevo usuario y contraseña"}