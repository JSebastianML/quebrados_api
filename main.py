from models.model_reg import RegisterIn, RegisterOut, deleteRegisterIn
from models.model_user import UserIn, UserOut, CreateUserIn
from db.users_db import db_user
from db.users_db import get_user, update_user, create_user_indb, eliminar_usuario
from db.reg_db import bd_register
from db.reg_db import save_register, find_register, delete_register, delete_user_registers, check_register, find_one_register
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
async def create_user(datosRegistro: CreateUserIn):
    user_exists = get_user(datosRegistro.name)
    if (user_exists!=None):
        return {"respuesta": "Lo sentimos, el nombre de usuario ya está en uso"}
    else:
        datosRegistro=db_user(**datosRegistro.dict(), total=0)
        create_user_indb(datosRegistro)
        return {"respuesta": "El usuario se registró correctamente. Por favor ingresa a continuación con tu nuevo usuario y contraseña"}

@quebrados_app.delete("/user/options/{user}")
async def delete_user(user: str):
    user_exists = get_user(user)
    if (user_exists!=None):
        eliminar_usuario(user)
        return {"respuesta": "El usuario y sus registros fueron eliminados"}
    else:
        return {"respuesta": "El usuario no existe"}
        

@quebrados_app.post("/register/delete")
async def delete_reg(datos: deleteRegisterIn):
    bandera = check_register(datos.user, datos.id_register)
    user_exists = get_user(datos.user)
    registro_aux = find_one_register(datos.id_register)

    if (bandera == True):
        if registro_aux.category == "ingreso":
            user_exists.total = user_exists.total - registro_aux.value
        elif registro_aux.category == "egreso":
            user_exists.total = user_exists.total + registro_aux.value

        update_user(user_exists)

        delete_register(datos.id_register)
        return {"respuesta":"Registo eliminado con éxito"}
    else:
        return {"respuesta":"el usuario "+datos.user+" no tiene registros con id "+str(datos.id_register)}


"""
@quebrados_app.get("/user/stats/{user}")
async def get_incomes_exp(user: str):
    user_exists = get_user(user)

    if user_exists==None:
        raise HTTPException(status_code=404, detail="El usuario no está registrado")

    match_list = find_register(user_exists.user) 

    cant_ingresos=0
    cant_egresos=0

    for reg in match_list:
        if(reg.category=="ingreso"):
            cant_ingresos+=1
        elif(reg.category=="egreso"):
            cant_egresos+=1
    
    total_ingresos=((cant_ingresos)/len(match_list))*100
    total_egresos=((cant_egresos)/len(match_list))*100

    return {"ingresos":total_ingresos, "egresos":total_egresos}
"""