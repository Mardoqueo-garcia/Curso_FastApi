from fastapi import FastAPI #importamos el modulo
from fastapi.responses import HTMLResponse, FileResponse #para retornar codigo html, fileresponse para retornar el archivo html, htmlresponse para retornar codigo escrito dentro de la funcion. 
import data #importamos para traer el archivo json
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
    return data.data #traemos el archivo de las peliculas

#Mediante parametros
@app.get('/movies/{movie_id}', tags=['Movies']) #dentro de las llaves le especificamos que parametro debe ingresar
def get_movies_by_id(movie_id : int): #de esta forma le definimos el parametro y el tipo de dato que debe recibir
    '''
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

    '''
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
@app.get('/movies/', tags=['Movies']) #le agregamos el slash a la ruta para que detecte qeu se agregara un parametro query y no nos remplace el otro metodo creado anteriormente.
def get_movies_by_category(category : str, year : int): #no ingresamos la variable dentro de la url ya que automaticamente fastapi lo detectara como un parametro query.

    #codigo 1 (mi aporte)
    for items in movies:
        if items['category']==category.lower and items['year']==year:
            return items
    return f"Movie not fount in year {year} by category {category}"

    '''
    #codigo 2 (aporte)
    #mostrando lista mediante list comprenhesion
    return [movie for movie in movies if movie['category'] == category]

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