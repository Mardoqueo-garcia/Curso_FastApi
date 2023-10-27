from fastapi.security import HTTPBearer #HttpBearer para la autenticacion del token
from starlette.requests import Request 
from fastapi import HTTPException, status
from Manager.jwt_manager import validate_token

class JWTBearer(HTTPBearer):
   async def __call__(self, request: Request):
        #desde la clase superior osea la principal HTTPBearer en la que estamos, vamos a llamar al metodo call, le pasamos la peticion. Al hacer eso tomara un tiempo por lo tando debemos hacer la función asincrona
        auth = await super().__call__(request) #obtenemos los datos de las credenciales con las que se generó el token
        data = validate_token(auth.credentials) #Validamos el token con las credenciales obtenidas
        if data['email'] != 'admin@gmail.com' or data['password'] != 'admin': #si los datos son diferentes, mandaremos una excepcion de credenciales invalidas
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Credenciales no validas, sorry')
