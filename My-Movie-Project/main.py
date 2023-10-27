#FASTAPI
from fastapi import Depends, FastAPI, HTTPException, Path, Query, status #HTTPException para mandar mensajes personalizados de codigo dependiendo del status_code. Path para hacer validaciones a los parametros. Query para las validaciones de los parametros query 
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse #para retornar codigo html, fileresponse para retornar el archivo html, htmlresponse para retornar codigo escrito dentro de la funcion. JsonResponde para mandar contenido en formato json 
from fastapi.encoders import jsonable_encoder #para convertir los datos en objetos

#Others
from pydantic import BaseModel, Field #BaseModel para crear esquemas de datos, Field es una funcion para validacion de datos a los campos del esquema
from typing import Optional, List #Para que podamos poner como opcional un dato. List para indicar que devolveremos una lista 
import datetime #modulo destinado a fechas

#MANAGER
from Manager.jwt_manager import create_token #importamos la funcion de generar el token
from Auth.auth import JWTBearer

#BASE DE DATOS
from config.database import Session, engine, Base
from models.movie import Movie_models
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title= "Movies Server --Beta",
    description= "Aca encontraras un servidor de peliculas Latinoamericanas usando una base de datos local.",
    version= "0.1.0"
)

#Creacion del modelo para datos del usuario
class User(BaseModel):
    email:str = Field(default='@gmail.com', min_length=13, max_length=20)
    password:str = Field(default='1234', min_length=4, max_length=12)

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
                'id':len(datass.Data) + 1,
                'title':'My new movie',
                'overview':'Descripcion breve',
                'year': 2022,
                'rating': 9.2,
                'category': 'accion'
            }
        }
    '''

@app.get('/', tags=['Home']) #nuestra ruta inicial, la etiqueta (tags) sirve para  agrupar determinadas rutas de nuestra aplicación
def message():
     return HTMLResponse( #Forma de retornar un html con codigo dentro de return
         '''<h1>PelisMar</h1>
           <p>Puedes ejecutar la documentación swagger colocando en la url de la web /docs. Eso te abrira la documentacion para que puedas ver todos los metodos de nuestro servidor.</p>
         ''')
    #return FileResponse('index.html') #De esta forma devolvemos un archivo html completo

#metodo para recibir los datos del usuario
@app.post('/login', tags=['Auth'])
def login(user : User): #recibira un usuario del tipo User
    if user.email == 'admin@gmail.com' and user.password == 'admin': #validamos datos de usuario
        token = create_token(user.model_dump()) #creamos el token, mandamos los datos convertidos a un diccionario usando la función model_dump()
        return JSONResponse(status_code=status.HTTP_200_OK, content=token) #retornamos ese token
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='email or password incorrect')

#METODOS GET (metodo para retornar todas las peliculas)
@app.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())]) #Le indicamos que el modelo de respuesta sera una lista de Movies, metodo protegido que depende de la clase JWTBearer()
def get_movies():
    try:
        db = Session() #Instancia de sesion
        result = db.query(Movie_models).all() #Nos traera todos los datos de la tabla Movie_models
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result)) #JSONResponse para mandar la información en contenido json, convertimos los datos de la tabla a objetos para poder verlos en la documentacion
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
#Mediante parametros
@app.get('/movies/{movie_id}', tags=['Movies'], response_model=Movie, status_code=status.HTTP_200_OK) #dentro de las llaves le especificamos que parametro debe ingresar. Le indicamos que el modelo de respuesta sera de la clase Movie
def get_movies_by_id(movie_id : int = Path(ge=1, le=12)): #Definimos el parametro y el tipo de dato que debe recibir, validamos el parametro
    try:
        db = Session()
        result = db.query(Movie_models).filter(Movie_models.id==movie_id).first() #filtramos los datos validando que sean del mismo id, first() ==> para que obtenga el primer resultado
        if not result: return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message':'No found by id'}) #validamos en caso de que no encuentre los datos mediante el id ingresado
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
#Metodo mediante parametros query
@app.get('/movies/category/', tags=['Movies'], response_model=List[Movie],status_code=status.HTTP_200_OK) #le agregamos el slash a la ruta para que detecte que se agregará un parametro query
def get_movies_by_category(category:str = Query(min_length=3, max_length=15)): #no ingresamos la variable dentro de la url ya que automaticamente fastapi lo detectará como un parametro query. Validamos el parametro query dandole un limite de caracteres
    try:
        db = Session()
        result = db.query(Movie_models).filter(Movie_models.category==category).all()
        if not result:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message':'Movie by category not Found'})
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#METODO POST (para registrar nuevas peliculas)
@app.post('/movies', tags=['Movies'], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie): #requerimos una pelicula de la clase Movie
    try:
        db = Session()
        new_movie = Movie_models(**movie.model_dump()) # ** <- para mandar los parametros y no escribiros manualmente
        db.add(new_movie) #agregamos la pelicula a nuestra base de datos
        db.commit() #hacemos una actualizacion para que se guarden los datos
        return JSONResponse({'Message': 'Creación exitosa'}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#METODO PUT (para actualizar una pelicula)
@app.put('/movies/{id_movie}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK) #pediremos el id como parametro
def update_movie(id_movie:int, movie : Movie):
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
@app.delete('/movies/{id_movie}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK) #La respuesta será un diccionario con un mensaje
def delete_movie(id_movie:int):
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