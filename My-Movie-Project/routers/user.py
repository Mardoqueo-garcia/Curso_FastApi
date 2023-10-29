#FASTAPI
from fastapi import APIRouter, HTTPException,status
from fastapi.responses import JSONResponse
#Others
from utils.jwt_manager import create_token #importamos la funcion de generar el token
from schemas.user import User

user_router = APIRouter()

#metodo para recibir los datos del usuario
@user_router.post('/login', tags=['Auth'])
def login(user : User): #recibira un usuario del tipo User
    if user.email == 'admin@gmail.com' and user.password == 'admin': #validamos datos de usuario
        token = create_token(user.model_dump()) #creamos el token, mandamos los datos convertidos a un diccionario usando la función model_dump()
        return JSONResponse(status_code=status.HTTP_200_OK, content=token) #retornamos ese token
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='email or password incorrect')