from config.database import Base
from sqlalchemy import Column, Integer, String, Float #Tipos de datos

class Movie_models(Base): #Movie_models heredará de Base, le estamos diciendo que sera una entidad de la base de datos
    
    __tablename__ = 'movies' #este será el nombre de nuestra tabla

    #Campos que tendra la tabla
    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)
