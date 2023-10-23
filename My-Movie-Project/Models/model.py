from pydantic import BaseModel, Field #BaseModel para crear esquemas de datos, Field es una funcion para validacion de datos a los campos del esquema
from typing import Optional, List #Para que podamos poner como opcional un dato. List para indicar que devolveremos una lista 
import datetime #modulo destinado a fechas
from Data import movies as db

#Creacion del modelo para datos del usuario
class User(BaseModel):
    email:str = Field(default='@gmail.com', min_length=13, max_length=20)
    password:str = Field(default='1234', min_length=4, max_length=12)

#Esquema de datos generales de las peliculas
class Movie(BaseModel):
    id : Optional[int] = None #para que el id sea opcional
    title : str = Field(min_length=5, max_length=20) #le estamos definiendo cual es el limite de caracteres para el titulo
    overview : str = Field(min_length=10, max_length=50)
    year : int = Field(ge=1980, le=datetime.date.today().year) #ge ==> para que el año ingresado sea mayor a 1980, le ==> para definir que el año debe ser menor o igual al año actual.
    rating : float = Field(ge=1, le=10.0)
    category : str = Field(min_length=5, max_length=10)

    #clase para definir los valores por defecto del body
    class Config:
        json_schema_extra = {
            'example':
            {
                'id':len(db.Data) + 1,
                'title':'My new movie',
                'overview':'Descripcion breve',
                'year': 2022,
                'rating': 9.2,
                'category': 'accion'
            }
        }
    #codigo debido al cambio de version a pydantic v2
    '''
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": len(db.Data) + 1,
                    "title": "New movie",
                    "overview": "Descripcion breve",
                    "year": 2022,
                    "rating":9.5,
                    "category": "accion"
                }
            ]
        }
    }
    '''