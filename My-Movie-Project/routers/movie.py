#FASTAPI
from fastapi import Depends, HTTPException, Path, Query, status, APIRouter #HTTPException para mandar mensajes personalizados de codigo dependiendo del status_code. Path para hacer validaciones a los parametros. Query para las validaciones de los parametros query 
from fastapi.responses import JSONResponse #JsonResponde para mandar contenido en formato json 
from fastapi.encoders import jsonable_encoder #para convertir los datos en objetos

#Others
from pydantic import BaseModel, Field #BaseModel para crear esquemas de datos, Field para validacion de datos a los campos del esquema
from typing import Optional, List #Para que podamos poner como opcional un dato. List para indicar que devolveremos una lista 
import datetime
from middleware.jwt_bearer import JWTBearer

#BASE DE DATOS
from models.movie import Movie_models
from config.database import Session

movie_router = APIRouter() #Creando una instancia de ApiRouter

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
'''
#Manejo de errores dentro de las rutas usando la documentacion 
@app.middleware("http")
async def add_process_time_header(request : Request, call_next):
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        return response
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'Error in':str(e)})
'''

#METODOS GET (metodo para retornar todas las peliculas)
@movie_router.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())]) #Le indicamos que el modelo de respuesta sera una lista de Movies, metodo protegido que depende de la clase JWTBearer()
def get_movies() -> List[Movie]:
    try:
        db = Session() #Instancia de sesion
        result = db.query(Movie_models).all() #Nos traera todos los datos de la tabla Movie_models
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result)) #JSONResponse para mandar la información en contenido json, convertimos los datos de la tabla a objetos con jsonable_encoder
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
#Mediante parametros
@movie_router.get('/movies/{movie_id}', tags=['Movies'], response_model=Movie, status_code=status.HTTP_200_OK) #dentro de las llaves le especificamos que parametro debe ingresar. Le indicamos que el modelo de respuesta sera de la clase Movie
def get_movies_by_id(movie_id : int = Path(ge=1, le=12)) -> Movie: #Definimos el parametro y el tipo de dato que debe recibir, validamos el parametro
    try:
        db = Session()
        result = db.query(Movie_models).filter(Movie_models.id==movie_id).first() #filtramos los datos validando que sean del mismo id, first() ==> para que obtenga el primer resultado
        if not result: return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message':'No found by id'}) #validamos en caso de que no encuentre los datos mediante el id ingresado
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
#Metodo mediante parametros query
@movie_router.get('/movies/category/', tags=['Movies'], response_model=List[Movie],status_code=status.HTTP_200_OK) #le agregamos el slash a la ruta para que detecte que se agregará un parametro query
def get_movies_by_category(category:str = Query(min_length=3, max_length=15)) -> List[Movie]: #no ingresamos la variable dentro de la url ya que automaticamente fastapi lo detectará como un parametro query. Validamos el parametro query dandole un limite de caracteres
    try:
        db = Session()
        result = db.query(Movie_models).filter(Movie_models.category==category).all()
        if not result:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message':'Movie by category not Found'})
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#METODO POST (para registrar nuevas peliculas)
@movie_router.post('/movies', tags=['Movies'], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> dict: #requerimos una pelicula de la clase Movie
    try:
        db = Session()
        new_movie = Movie_models(**movie.model_dump()) # ** <- para mandar los parametros y no escribiros manualmente
        db.add(new_movie) #agregamos la pelicula a nuestra base de datos
        db.commit() #hacemos una actualizacion para que se guarden los datos
        return JSONResponse({'Message': 'Creación exitosa'}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#METODO PUT (para actualizar una pelicula)
@movie_router.put('/movies/{id_movie}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK) #pediremos el id como parametro
def update_movie(id_movie:int, movie : Movie) -> dict:
    try:
        db = Session()
        result = db.query(Movie_models).filter(Movie_models.id==id_movie).first()
        if not result:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message':'Movie by id not found in database'})
        result.title = movie.title
        result.overview = movie.overview
        result.rating = movie.rating
        result.year = movie.year
        result.category = movie.category
        db.commit()
        return JSONResponse(content={'message':'Modificacion exitosa'})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#METODO DELETE (para eliminar una pelicula mediante el id que nos manden)
@movie_router.delete('/movies/{id_movie}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK) #La respuesta será un diccionario con un mensaje
def delete_movie(id_movie:int) -> dict:
    try:
        db = Session()
        result = db.query(Movie_models).filter(Movie_models.id==id_movie).first()
        if not result:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message':'Remove by id not found'})
        db.delete(result) #le mandamos los datos a eliminar
        db.commit() #subimos los cambios para actualizar los datos
        return JSONResponse({'Message': 'Eliminación exitosa'})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))