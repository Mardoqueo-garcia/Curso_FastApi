from fastapi import FastAPI #importamos el modulo
from fastapi.responses import HTMLResponse, FileResponse #para retornar codigo html

#Manera 1
'''
app = FastAPI() #creamos una instancia de fastapi almacenada en la variable app
app.title = "Movies server --Beta" #nombre que se le da al titulo de nuestra documentacion en la web.
app.version = "0.0.1" #Le estamos escribiendo la version actual que tiene nuestro servidor
'''
#Manera 2
app = FastAPI(
    title= "Movies Server --Beta",
    description= "Aca encontraras el listado de las peliculas, por: -Categorias -Mas votadas -Estrenos",
    version= "0.0.1"
)

#diccionario de la informacion de las peliculas
movies = [
    {
        'id':1,
        'Title':'Step up 3',
        'Overview':'El baile callejero underground de Nueva York constituye el...',
        'year': '2010',
        'rating':8.9,
        'category': "Baile"
    },
    {
        'id':2,
        'Title':'Asi en la tierra como en el infierno',
        'Overview':'La arqueóloga Scarlett Marlowe ha dedicado toda su vida a encontrar...',
        'year': '2014',
        'rating':9.1,
        'category': "Terror"
    }
]


#METODOS GET
@app.get('/', tags=['Home']) #nuestra ruta inicial, la etiqueta (tags) sirve para  agrupar determinadas rutas de nuestra aplicación
def message(): #funcion del endpoint
    return FileResponse('index.html') # de esta forma devolvemos un archivo html completo para mayor facilidad

#metodo para retornar todas las peliculas
@app.get('/movies', tags=['Movies'])
def get_movies():
    return movies

#metodo que recibira un parametro al acceder a esa url
@app.get('/movies/{movie_id}', tags=['Movies']) #dentro de las llaves le especificamos que parametro debe ingresar
def get_movies(movie_id : int): #de esta forma le definimos el parametro y el tipo de dato que debe recibir
    #codigo 1 (de la clase)
    for item in movies: #iteramos la lista de las peliculas
        if item['id']==movie_id: #validamos si el id ingresado esta en el id del listado
            return item #si ese fuese el caso, nos retornara la informacion de la pelicula basada en ese id
    return 'El id ingresado no existe' #de lo contrario nos arrojara un mensaje
    
    #codigo 2 (aporte del compañero)
    '''
    try:
        return movies[movie_id - 1]
    except IndexError:
        return {"error": "Movie not found"}
    '''
    #codigo 3 (aporte del compañero)
    '''
    movie = list(filter(lambda x: x['id'] == movie_id,movies))
    return "Movie not found" if not movie else movie[0]
    '''
