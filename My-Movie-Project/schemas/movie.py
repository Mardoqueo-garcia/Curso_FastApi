from pydantic import BaseModel, Field #BaseModel para crear esquemas de datos, Field para validacion de datos a los campos del esquema
from typing import Optional #Para que podamos poner como opcional un dato
import datetime

#Esquema de datos generales de las peliculas
class Movie(BaseModel):
    id : Optional[int] = None #para que el id sea opcional
    title : str = Field(default='My new Movie',min_length=5, max_length=20) #le estamos definiendo cual es el limite de caracteres para el titulo
    overview : str = Field(default='Decripcion breve',min_length=10, max_length=50)
    year : int = Field(default='2022',ge=1980, le=datetime.date.today().year) #ge ==> para que el año ingresado sea mayor a 1980, le ==> para definir que el año debe ser menor o igual al año actual.
    rating : float = Field(default=8.5,ge=1, le=10.0)
    category : str = Field(default='accion',min_length=3, max_length=10)

    #clase para definir los valores por defecto del body
    '''
    class Config:
        json_schema_extra = {
            'example':
            {
                'id':7,
                'title':'My new movie',
                'overview':'Descripcion breve',
                'year': 2022,
                'rating': 9.2,
                'category': 'accion'
            }
        }
    '''