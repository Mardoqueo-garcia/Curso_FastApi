#FASTAPI
from fastapi import APIRouter, HTTPException,status
from fastapi.responses import JSONResponse
#Others
from pydantic import BaseModel, Field
from Manager.jwt_manager import create_token #importamos la funcion de generar el token

user_router = APIRouter()

#Creacion del modelo para datos del usuario
class User(BaseModel):
    email:str = Field(default='@gmail.com', min_length=13, max_length=20)
    password:str = Field(default='1234', min_length=4, max_length=12)

#metodo para recibir los datos del usuario
@user_router.post('/login', tags=['Auth'])
def login(user : User): #recibira un usuario del tipo User
    if user.email == 'admin@gmail.com' and user.password == 'admin': #validamos datos de usuario
        token = create_token(user.model_dump()) #creamos el token, mandamos los datos convertidos a un diccionario usando la función model_dump()
        return JSONResponse(status_code=status.HTTP_200_OK, content=token) #retornamos ese token
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='email or password incorrect')