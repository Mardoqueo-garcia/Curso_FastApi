from fastapi import FastAPI, Body, HTTPException #Importamos la clase body para requerimientos en el cuerpo de la peticion, HTTPException para mansar mensajes personalizados de codigo dependiendo del status_code.
from fastapi.responses import HTMLResponse, FileResponse #para retornar codigo html, fileresponse para retornar el archivo html, htmlresponse para retornar codigo escrito dentro de la funcion. 
from pydantic import BaseModel, Field #BaseModel para crear esquemas de datos, Field es una clase para validacion de datos.
from typing import Optional #Para que podamos poner como opcional un dato
import movies as db #importamos la base de datos de las peliculas
import datetime #modulo destinado a fechas

#Esquema de datos generales de las peliculas
class Movie(BaseModel):
    id : Optional[int] = None #para que el id sea opcional
    title : str = Field(min_length=5, max_length=20) #le estamos definiendo cual es el linite de caracteres de para el titulo
    overview : str = Field(min_length=10, max_length=50)
    year : int = Field(ge=1980, le=datetime.date.today().year) #ge ==> para que el año ingresado sea mayor a 1980, le ==> para definir que el año debe ser menor o igual a 2022.
    rating : float = Field(ge=0, le=9.9)
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

#METODOS GET
@app.get('/', tags=['Home']) #nuestra ruta inicial, la etiqueta (tags) sirve para  agrupar determinadas rutas de nuestra aplicación
def message():
    #Forma de retornar un html con codigo dentro de return
     return HTMLResponse(
         '''<h1>PelisMar</h1>
           <h4>Servidor de peliculas del cine Latinoamericano</h4>
           <p>Puedes ejecutar la documentación swagger colocando en la url de la web /docs. Eso te abrira la documentacion para que puedas ver todos los metodos de nuestro servidor.</p>
         ''')
    #return FileResponse('index.html') #De esta forma devolvemos un archivo html completo

#metodo para retornar todas las peliculas
@app.get('/movies', tags=['Movies'])
def get_movies():
    return movies

#Mediante parametros
@app.get('/movies/{movie_id}', tags=['Movies']) #dentro de las llaves le especificamos que parametro debe ingresar
def get_movies_by_id(movie_id : int): #de esta forma le definimos el parametro y el tipo de dato que debe recibir
    response = [item for item in movies if item['id']==movie_id]
    if len(response) > 0: return response
    raise HTTPException(status_code=404, detail='Id not Found') #nos retornara codigo de error y su mensaje personalizado
    
#Metodo mediante parametros query
@app.get('/movies/category/', tags=['Movies']) #le agregamos el slash a la ruta para que detecte que se agregara un parametro query y no nos remplace el otro metodo creado anteriormente.
def get_movies_by_category(category:str): #no ingresamos la variable dentro de la url ya que automaticamente fastapi lo detectara como un parametro query.
    response = [movie for movie in movies if movie['category']==category]
    if len(response) > 0: return response
    raise HTTPException(status_code=404, detail='Movie by category not Found')

#Para buscar mediante año de publicacion
@app.get('/movies/publicate/{movie_year}', tags=['Movies'])
def get_movie_by_year(movie_year : int):
    response = [items for items in movies if items['year']==movie_year]
    if len(response) > 0: return response
    raise HTTPException(status_code=404, detail='Movie by year not Found')
    
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
@app.post('/movies', tags=['Movies'])
def create_movie(movie: Movie): #requerimos una pelicula de la clase Movie
    movies.append(movie) #de esta manera registramos directamente la pelicula.
    return movies

#METODO PUT (para actualizar una pelicula)
@app.put('/movies/{id}', tags=['Movies']) #pediremos el id como parametro
def update_movie(id:int, movie : Movie):
    for items in movies:
        if items["id"]==id:
            items["title"]=movie.title
            items["overview"]=movie.overview
            items["year"]=movie.year
            items["rating"]=movie.rating
            items["category"]=movie.category
            return movies
    raise HTTPException(status_code=404, detail='Movie by id not found in database')

#METODO DELETE (para eliminar una pelicula mediante el id que nos manden)
@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id:int):
    for items in movies:
        if items["id"]==id:
            movies.remove(items)
            return movies
    raise HTTPException(status_code=404, detail='Remove by id not found')