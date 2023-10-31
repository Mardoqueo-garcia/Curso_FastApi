#FASTAPI
import os
from fastapi import FastAPI
import uvicorn

#MODULOS LOCALES
from middleware.error_handler import ErrorHandler
from routers import home, movie, user

#BASE DE DATOS
from config.database import engine, Base
Base.metadata.create_all(bind=engine)

#Configuracion 
app = FastAPI()
app.title = "Movies Server --Beta"
app.description = "Aca encontraras un servidor de peliculas Latinoamericanas usando una base de datos local."
app.version = "0.2.1"

app.middleware(ErrorHandler) #Agregamos el manejador de errores creado

#Inclusion de routers
app.include_router(home.home_router) #Incluimos nuestra ruta principal
app.include_router(user.user_router) #Incluimos nuestras rutas del login
app.include_router(movie.movie_router) #Incluimos nuestras rutas de las movies

#Ejecutar la aplicacion al servidor RailWay
if __name__ == "__main__":
    uvicorn.run("main:app",
                port=int(os.environ.get("PORT", 8000)))