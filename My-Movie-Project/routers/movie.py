#FASTAPI
from fastapi import Depends, HTTPException, Path, Query, status, APIRouter #HTTPException para mandar mensajes personalizados de codigo dependiendo del status_code. Path para hacer validaciones a los parametros. Query para las validaciones de los parametros query 
from fastapi.responses import JSONResponse #JsonResponde para mandar contenido en formato json 
from fastapi.encoders import jsonable_encoder #para convertir los datos en objetos

#Others
from middleware.jwt_bearer import JWTBearer
from typing import List #List para indicar que devolveremos una lista 

#BASE DE DATOS
from models.movie import Movie_models
from config.database import Session
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter() #Creando una instancia de ApiRouter

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
        result = MovieService(db).get_movies() #Nos traera todos los datos de la tabla Movie_models
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result)) #JSONResponse para mandar la información en contenido json, convertimos los datos de la tabla a objetos con jsonable_encoder
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
#Mediante parametros
@movie_router.get('/movies/{movie_id}', tags=['Movies'], response_model=Movie, status_code=status.HTTP_200_OK) #dentro de las llaves le especificamos que parametro debe ingresar. Le indicamos que el modelo de respuesta sera de la clase Movie
def get_movies_by_id(movie_id : int = Path(ge=1, le=12)) -> Movie: #Definimos el parametro y el tipo de dato que debe recibir, validamos el parametro
    try:
        db = Session()
        #result : Movie_models = db.query(Movie_models).filter(Movie_models.id == movie_id).first()
        result = MovieService(db).get_movie_id(movie_id) #Le pasamos el parametro id requerido
        if not result: return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message':'No found by id'}) #validamos en caso de que no encuentre los datos mediante el id ingresado
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
#Metodo mediante parametros query
@movie_router.get('/movies/category/', tags=['Movies'], response_model=List[Movie],status_code=status.HTTP_200_OK) #le agregamos el slash a la ruta para que detecte que se agregará un parametro query
def get_movies_by_category(category:str = Query(min_length=3, max_length=15)) -> List[Movie]: #no ingresamos la variable dentro de la url ya que automaticamente fastapi lo detectará como un parametro query. Validamos el parametro query dandole un limite de caracteres
    try:
        db = Session()
        result = MovieService(db).get_movie_category(category)
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
        MovieService(db).create_movie(movie)
        return JSONResponse({'Message': 'Creación exitosa'}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#METODO PUT (para actualizar una pelicula)
@movie_router.put('/movies/{id_movie}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK) #pediremos el id como parametro
def update_movie(id_movie:int, movie : Movie) -> dict:
    try:
        db = Session()
        result = MovieService(db).get_movie_id(id_movie) #Obtenemos los datos con el id
        if not result: #Si no encuentra datos
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message':'Movie by id not found in database'})
        MovieService(db).update_movie(id_movie, movie) #Si los encuentra hacemos la modificacion
        return JSONResponse(content={'message':'Modificacion exitosa'})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#METODO DELETE (para eliminar una pelicula mediante el id que nos manden)
@movie_router.delete('/movies/{id_movie}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK) #La respuesta será un diccionario con un mensaje
def delete_movie(id_movie:int) -> dict:
    try:
        db = Session()
        result = MovieService(db).get_movie_id(id_movie)
        if not result:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message':'Remove by id not found'})
        MovieService(db).delete_movie(id_movie)
        return JSONResponse({'Message': 'Eliminación exitosa'})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))