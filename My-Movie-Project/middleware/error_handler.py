from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

class ErrorHandler(BaseHTTPMiddleware):
    #Creamos un metodo constructor
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app) #El metodo super es BaseHTTPMiddleware

    #Metodo que estará detectando los errores en nuestra aplicación
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse: #request: Request ==> para acceder a todos los request de la app, Response ==> en caso de que no haya un error le mandaremos una repuesta y en caso de que suceda un error le mandaremos una respuesta en formato json
        try:
            return await call_next(request) #Si no ocurre error retornara esta llamada
        except Exception as e:
            return JSONResponse(status_code=500, content={'Error': str(e)}) 