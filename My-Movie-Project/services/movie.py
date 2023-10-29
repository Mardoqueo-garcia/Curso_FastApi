from models.movie import Movie_models
from schemas.movie import Movie

class MovieService():
    #metodo constructor
    def __init__(self, db) -> None: #cada vez que se llame a este servicio se envie una sesion a la db
        self.db = db #le asignamos lo que llega como la db, con esto ya tendriamos acceso a la db para que pueda ser accesible a otros metodos de este servicio
    
    #metodo para obtener las pelis
    def get_movies(self): #Self es un metodo de instancia
        result = self.db.query(Movie_models).all()
        return result
    
    #Para filtrar por el id
    def get_movie_id(self, id):
        result = self.db.query(Movie_models).filter(Movie_models.id==id).first() #first() ==> para que obtenga el primer resultado
        return result
    
    #Para filtrar por categoria
    def get_movie_category(self, category):
        result = self.db.query(Movie_models).filter(Movie_models.category==category).all() #all() ==> para que obtenga todos los resultados
        return result
    
    #Para agregar una nueva pelicula
    def create_movie(self, movie : Movie): #recibiremos una movie del tipo Movie de nuestro modelo
        new_movie = Movie_models(**movie.model_dump()) #con ** las propiedades seran leias como parametros
        self.db.add(new_movie) #agregamos los datos a nuestra base de datos
        self.db.commit() #Hacemos una actualizacion para subir esos datos
        return #ya estan guardados los datos asi que solo retornamos

    #Para la actualizacion de los datos
    def update_movie(self, id : int, data : Movie):
        movie = self.db.query(Movie_models).filter(Movie_models.id == id).first() #filtramos los datos mediante el id
        
        #Los datos de la db seran igual a los datos que nos pasen
        movie.title = data.title
        movie.overview = data.overview
        movie.rating = data.rating
        movie.year = data.year
        movie.category = data.category

        self.db.commit()
        return

    #Para la eliminacion de la pelicula
    def delete_movie(self, id : int):
        result = self.db.query(Movie_models).filter(Movie_models.id == id).first()
        self.db.delete(result)
        #result = self.db.query(Movie_models).filter(Movie_models.id == id).delete() <= de esta forma tambien podemos hacer la eliminacion
        self.db.commit()
        return
