from fastapi import FastAPI, Body #importamos el modulo
from fastapi.responses import HTMLResponse, FileResponse #para retornar codigo html, fileresponse para retornar el archivo html, htmlresponse para retornar codigo escrito dentro de la funcion. 
import data #importamos para traer el archivo json
#movies = data.data #almacenamos la informacion en la variable movies
#Manera 1
'''
app = FastAPI() #creamos una instancia de fastapi almacenada en la variable app
app.title = "Movies server --Beta" #nombre que se le da al titulo de nuestra documentacion en la web.
app.version = "0.0.1" #Le estamos escribiendo la version actual que tiene nuestro servidor
'''
#Manera 2
app = FastAPI(
    title= "Movies Server --Beta",
    description= "Aca encontraras un servidor de peliculas, por: -Categorias -Mejor puntuacion -Por año",
    version= "0.0.2"
)


#diccionario de la informacion de las peliculas
movies = [
    {
        'id':1,
        'title':'Step up 3',
        'overview':'El baile callejero underground de Nueva York constituye el...',
        'year': 2010,
        'rating':8.9,
        'category': "baile"
    },
    {
        'id':2,
        'title':'Asi en la tierra como en el infierno',
        'overview':'La arqueóloga Scarlett Marlowe ha dedicado toda su vida a encontrar...',
        'year': 2014,
        'rating':8.1,
        'category': "terror"
    },
    {
        'id':3,
        'title':'Triunfos robados',
        'overview':'La estudiante de primer año de la universidad Whittier y su amiga Monica forman parte...',
        'year': 2004,
        'rating':8.1,
        'category': "baile"
    },
    {
        'id':4,
        'title':'Camino hacia el terror',
        'overview':'En un lugar de Chernobyl, era un pueblo olvidado debido a que...',
        'year': 2002,
        'rating':9.0,
        'category': "terror"
    },
    {
        'id':5,
        'title':'El Unico',
        'overview':'Jhon es un policia que trabaja sin preocupaciones de nada, sin embargo un dia de...',
        'year': 2010,
        'rating':8.1,
        'category': "accion"
    }
]



#METODOS GET
@app.get('/', tags=['Home']) #nuestra ruta inicial, la etiqueta (tags) sirve para  agrupar determinadas rutas de nuestra aplicación
def message():
    #Forma de retornar un html con codigo dentro de return
     return HTMLResponse(
         '''<h1>PelisMar</h1>
           <h4>Servidor de diversas peliculas del cine Latinoamericano</h4>
           <p>Puedes ejecutar la documentación swagger colocando en la url de la web /docs. Eso te abrira la documentacion para que puedas ver todos los metodos de nuestro servidor.</p>
         ''')

    #return FileResponse('index.html') #De esta forma devolvemos un archivo html completo

#metodo para retornar todas las peliculas
@app.get('/movies', tags=['Movies'])
def get_movies():
    return movies #traemos el archivo de las peliculas

#Mediante parametros
@app.get('/movies/{movie_id}', tags=['Movies']) #dentro de las llaves le especificamos que parametro debe ingresar
def get_movies_by_id(movie_id : int): #de esta forma le definimos el parametro y el tipo de dato que debe recibir
    #codigo 1 (de la clase)
    for item in movies: #iteramos la lista de las peliculas
        if item['id']==movie_id: #validamos si el id ingresado esta en el id del listado
            return item #si ese fuese el caso, nos retornara la informacion de la pelicula basada en ese id
    return 'El id ingresado no existe' #de lo contrario nos arrojara un mensaje
    
    '''
    #codigo de prueba(mio)
    try:
        return movies[movie_id -1]
    except :
        countt = len(movies)
        return f"Error, limite de id es {countt}"

    #codigo 2 (aporte)
    try:
        return movies[movie_id - 1]
    except IndexError:
        return {"error": "Movie not found"}
    
    #codigo 3 (aporte)
    movie = list(filter(lambda x: x['id'] == movie_id,movies))
    return "Movie not found" if not movie else movie[0]
    '''
#Metodo mediante parametros query
@app.get('/movies/', tags=['Movies']) #le agregamos el slash a la ruta para que detecte que se agregara un parametro query y no nos remplace el otro metodo creado anteriormente.
def get_movies_by_category(category:str, year:int): #no ingresamos la variable dentro de la url ya que automaticamente fastapi lo detectara como un parametro query.

    #codigo 1 (mi aporte)
    try: 
        response = [movie for movie in movies if movie['category']==category and movie['year']==year]
        if len(response) > 0: return response
        else: return 'Movies no found by category and year'
    except: 
        return 'Error en el servidor remoto'

    '''
    #codigo 2 (aporte)
    #mostrando lista mediante list comprenhesion
    response = [movie for movie in movies if movie['category'] == category]
    if len(response) > 0:
        return response
    else:
        return "Movies not found"

    #codigo 3 (aporte)
    #mostrando la lista mediante la funcion filter
    return list(filter(lambda item: item['category'] == category , movies))

    #codigo 4 (aporte)
    # Filtrar las películas por categoría y año
    filtered_movies = [movie for movie in movies if movie['category'] == category and movie['year'] == year]
    # Si hay películas que cumplen (o sea la lista tiene elementos)
    if filtered_movies:
        return filtered_movies
    return f'No hay películas para la categoría {category} y el año {year}'
    '''

#METODO POST
@app.post('/movies', tags=['Movies'])
#para registrar nuevas peliculas
#Codigo de la clase
#El body nos sirve para que los parametros no se tomen como un parametro query si no como peticion del body, el default es lo que nos mostrara por defecto en el body
def create_movie(id:int = Body(default=len(movies)+1), title:str = Body(default="Text"), overview:str = Body(default="Text"), year:int = Body(default=2023), rating:float = Body(default=5.0), category:str = Body(default='Text')):
    #agregamos a nuestra lista de las peliculas
    movies.append({
        "id":id,
        "title":title,
         "overview":overview,
         "year":year,
         "rating":rating,
         "category":category
     })
    return movies

'''
#Codigo 2 (Aporte)
from pydantic import BaseModel #para crear el modelo
class Movie(BaseModel): #creamos una clase donde estaran las variables que usaremos como parametros
    id:int
    title:str
    overview:str
    year:int
    rating:float
    category:str
@app.post('/movies', tags=['Movies'],response_model = list[Movie]) #agregamos una lista del modelo
def create_movie(new_movie: Movie):
    movies.append(new_movie)
    return movies
'''

#METODO PUT
#para actualizar una pelicula
@app.put('/movies/{id}', tags=['Movies']) #pediremos el id como parametro
def update_movie(id:int, title:str = Body(default="Text"), overview:str = Body(default="Text"), year:int = Body(default=2023), rating:float = Body(default=5.0), category:str = Body(default='Text')):
    for items in movies:
        if items["id"]==id:
            items["title"]=title
            items["overview"]=overview
            items["year"]=year
            items["rating"]=rating
            items["category"]=category
            return movies
    return "Movie by id not found"

'''
#mi codigo de aporte al reto
from pydantic import BaseModel
class Items(BaseModel):
    title:str
    overview:str
    year:int
    rating:int
    category:str
@app.put('/movies/{id_movie}',tags=['Movies'])
def update_movie(id_movie:int, movie:Items):
    return {'id':id_movie, 'title':movie.title, 'overview':movie.overview, 'year':movie.year, 'rating':movie.rating, 'category':movie.category}
'''

#METODO DELETE
#para eliminar una pelicula mediante el id que nos manden
@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id:int):
    for items in movies:
        if items["id"]==id:
            movies.remove(items)
            return movies

'''
#Codigo de aporte al reto
@app.delete('/movies/{id_movie}', tags=['Movies'])
def delete_movie(id_movie: int):
    for item in movie:
        if item["id"]==id:
            movies.remove(item)
            return movies
    return "Error, id not found"
'''