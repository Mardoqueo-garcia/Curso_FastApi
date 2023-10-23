#FASTAPI
from fastapi import Depends, FastAPI, HTTPException, Path, Query, status #Importamos HTTPException para mandar mensajes personalizados de codigo dependiendo del status_code. Path para hacer validaciones a los parametros. Query para las validaciones de los parametros quey 
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse #para retornar codigo html, fileresponse para retornar el archivo html, htmlresponse para retornar codigo escrito dentro de la funcion. JsonResponde para mandar contenido en formato json 

#MODELS
from Models.model import User, Movie
#PYTHON
from typing import List
import Data.movies as db #importamos la base de datos de las peliculas
#MANAGER
from Manager.jwt_manager import create_token #importamos la funcion de generar el token
from Auth.auth import JWTBearer

app = FastAPI(
    title= "Movies Server --Beta",
    description= "Aca encontraras un servidor de peliculas Latinoamericanas usando una base de datos local.",
    version= "0.1.0"
)

movies =db.Data #importamos las peliculas.

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
    if user.email == 'admin@gmail.com' and user.password == 'admin': #simulamos un usuario
        token = create_token(user.model_dump()) #creamos el token, mandando los datos convertidos a un diccionario, model_dump() para retornar el diccionario
        return JSONResponse(status_code=status.HTTP_200_OK, content=token) #retornamos ese token
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='email or password incorrect')

#METODOS GET (metodo para retornar todas las peliculas)
@app.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())]) #Le indicamos que el modelo de respuesta sera una lista de Movies
def get_movies():
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content=movies) #de esta forma estamos mandando la informacion en contenido json
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error Unauthorized')
#Mediante parametros
@app.get('/movies/{movie_id}', tags=['Movies'], response_model=Movie, status_code=status.HTTP_200_OK) #dentro de las llaves le especificamos que parametro debe ingresar. Le indicamos que el modelo de respuesta sera de la clase Movie
def get_movies_by_id(movie_id : int = Path(ge=1, le=12)): #de esta forma le definimos el parametro y el tipo de dato que debe recibir, validamos el parametro dando limite >= 1 o <= a la cantidad de id de la db
    response = [item for item in movies if item['id']==movie_id]
    if len(response) > 0: return JSONResponse(response)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id not Found') #nos retornara codigo de error y su mensaje personalizado
    
#Metodo mediante parametros query
@app.get('/movies/category/', tags=['Movies'], response_model=List[Movie],status_code=status.HTTP_200_OK) #le agregamos el slash a la ruta para que detecte que se agregara un parametro query y no nos remplace el otro metodo creado anteriormente.
def get_movies_by_category(category:str = Query(min_length=6, max_length=15)): #no ingresamos la variable dentro de la url ya que automaticamente fastapi lo detectara como un parametro query. Validamos el parametro query dandole un limite de caracteres
    response = [movie for movie in movies if movie['category']==category]
    if len(response) > 0: return JSONResponse(response)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie by category not Found')

#METODO POST (para registrar nuevas peliculas)
@app.post('/movies', tags=['Movies'], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie): #requerimos una pelicula de la clase Movie
    try:
        movies.append(movie.model_dump()) #de esta manera registramos directamente la pelicula. Lo convertimos a diccionario para que no nos genere error al iterarlo ya que lo crea como un objeto
        return JSONResponse({'Message': 'Created Movie'}, status_code=status.HTTP_201_CREATED)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Error created movie')

#METODO PUT (para actualizar una pelicula)
@app.put('/movies/{id_movie}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK) #pediremos el id como parametro
def update_movie(id_movie:int, movie : Movie):
    for items in movies:
        if items["id"]==id_movie:
            items["title"]=movie.title
            items["overview"]=movie.overview
            items["year"]=movie.year
            items["rating"]=movie.rating
            items["category"]=movie.category
            return JSONResponse({'Message' : 'Update Movie'})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie by id not found in database')

#METODO DELETE (para eliminar una pelicula mediante el id que nos manden)
@app.delete('/movies/{id_movie}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK) #La respuesta sera un diccionario con un mensaje
def delete_movie(id_movie:int):
    for items in movies:
        if items["id"]==id_movie:
            movies.remove(items)
            return JSONResponse({'Message': 'Eliminacion exitosa'})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Remove by id not found')