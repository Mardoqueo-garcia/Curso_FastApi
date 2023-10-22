from fastapi import FastAPI, Body, HTTPException, Path, Query, status #Importamos la funcion body para requerimientos en el cuerpo de la peticion, HTTPException para mandar mensajes personalizados de codigo dependiendo del status_code. Path para hacer validaciones a los parametros. Query para las validaciones de los parametros quey 
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse #para retornar codigo html, fileresponse para retornar el archivo html, htmlresponse para retornar codigo escrito dentro de la funcion. JsonResponde para mandar contenido en formato json 
from pydantic import BaseModel, Field #BaseModel para crear esquemas de datos, Field es una funcion para validacion de datos a los campos del esquema
from typing import Optional, List #Para que podamos poner como opcional un dato. List para indicar que devolveremos una lista 
import datetime #modulo destinado a fechas
import Data.movies as db #importamos la base de datos de las peliculas
from Manager.jwt_manager import create_token #importamos la funcion de generar el token


#Creacion del modelo para datos del usuario
class User(BaseModel):
    email:str = Field(default='@gmail.com', min_length=13, max_length=20)
    password:str = Field(default='12345', min_length=4, max_length=12)

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

app = FastAPI(
    title= "Movies Server --Beta",
    description= "Aca encontraras un servidor de peliculas Latinoamericanas usando una base de datos local.",
    version= "0.0.2"
)

movies =db.Data #importamos las peliculas.

@app.get('/', tags=['Home']) #nuestra ruta inicial, la etiqueta (tags) sirve para  agrupar determinadas rutas de nuestra aplicación
def message():
    #Forma de retornar un html con codigo dentro de return
     return HTMLResponse(
         '''<h1>PelisMar</h1>
           <h4>Servidor de peliculas del cine Latinoamericano</h4>
           <p>Puedes ejecutar la documentación swagger colocando en la url de la web /docs. Eso te abrira la documentacion para que puedas ver todos los metodos de nuestro servidor.</p>
         ''')
    #return FileResponse('index.html') #De esta forma devolvemos un archivo html completo

#metodo para recibir los datos del usuario
@app.post('/login', tags=['Auth'])
def login(user : User): #recibira un usuario del tipo User
    if user.email == 'admin@gmail.com' and user.password == 'admin': #simulamos un usuario
        token = create_token(user.model_dump()) #creamos ese token, mandandole el los datos convertidos a un diccionario, model_dump() para diccionarios por los nuevos estandares
    return JSONResponse(status_code=status.HTTP_200_OK, content=token) #retornamos ese token

#METODOS GET
#metodo para retornar todas las peliculas
@app.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=status.HTTP_201_CREATED) #Le indicamos que el modelo de respuesta sera una lista de Movies
def get_movies():
    return JSONResponse(content=movies) #de esta forma estamos mandando la informacion en contenido json

#Mediante parametros
@app.get('/movies/{movie_id}', tags=['Movies'], response_model=Movie, status_code=status.HTTP_200_OK) #dentro de las llaves le especificamos que parametro debe ingresar. Le indicamos que el modelo de respuesta sera de la clase Movie
def get_movies_by_id(movie_id : int = Path(ge=1, le=len(db.Data))): #de esta forma le definimos el parametro y el tipo de dato que debe recibir, validamos el parametro dando limite >= 1 o <= a la cantidad de id de la db
    response = [item for item in movies if item['id']==movie_id]
    if len(response) > 0: return JSONResponse(response)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id not Found') #nos retornara codigo de error y su mensaje personalizado
    
#Metodo mediante parametros query
@app.get('/movies/category/', tags=['Movies'], response_model=List[Movie],status_code=status.HTTP_200_OK) #le agregamos el slash a la ruta para que detecte que se agregara un parametro query y no nos remplace el otro metodo creado anteriormente.
def get_movies_by_category(category:str = Query(min_length=6, max_length=15)): #no ingresamos la variable dentro de la url ya que automaticamente fastapi lo detectara como un parametro query. Validamos el parametro query dandole un limite de caracteres
    response = [movie for movie in movies if movie['category']==category]
    if len(response) > 0: return JSONResponse(response)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie by category not Found')

#Para buscar mediante año de publicacion
@app.get('/movies/publicate/{movie_year}', tags=['Movies'], response_model=List[Movie], status_code=status.HTTP_200_OK)
def get_movie_by_year(movie_year : int):
    response = [items for items in movies if items['year']==movie_year]
    if len(response) > 0: return JSONResponse(response)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie by year not Found')
    
    '''
    #codigo 2 (aporte)
    #mostrando la lista mediante la funcion filter
    return list(filter(lambda item: item['category'] == category , movies))

    #codigo 3 (aporte)
    # Filtrar las películas por categoría y año
    filtered_movies = [movie for movie in movies if movie['category'] == category and movie['year'] == year]
    # Si hay películas que cumplen (o sea la lista tiene elementos)
    if filtered_movies:
        return filtered_movies
    return f'No hay películas para la categoría {category} y el año {year}'
    '''

#METODO POST (para registrar nuevas peliculas)
@app.post('/movies', tags=['Movies'], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie): #requerimos una pelicula de la clase Movie
    movies.append(movie.model_dump()) #de esta manera registramos directamente la pelicula. Lo convertimos a diccionario para que no nos genere error al iterarlo ya que lo crea como un objeto
    return JSONResponse({'Message': 'Registro exitoso'})

#METODO PUT (para actualizar una pelicula)
@app.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK) #pediremos el id como parametro
def update_movie(id:int, movie : Movie):
    for items in movies:
        if items["id"]==id:
            items["title"]=movie.title
            items["overview"]=movie.overview
            items["year"]=movie.year
            items["rating"]=movie.rating
            items["category"]=movie.category
            return JSONResponse({'Message' : 'Modificacion exitosa'})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie by id not found in database')

#METODO DELETE (para eliminar una pelicula mediante el id que nos manden)
@app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK) #La respuesta sera un diccionario con un mensaje
def delete_movie(id:int):
    for items in movies:
        if items["id"]==id:
            movies.remove(items)
            return JSONResponse({'Message': 'Eliminacion exitosa'})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Remove by id not found')