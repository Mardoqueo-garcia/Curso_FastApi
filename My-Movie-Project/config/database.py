#Librerias
import os
from sqlalchemy import create_engine #create_engine ==> funcion para crear el motor de la base de datos
from sqlalchemy.orm.session import sessionmaker #Sesion de conexion a la base de datos
from sqlalchemy.ext.declarative import declarative_base #Para poder manipular todas las tablas 

sqlite_file_name = '../database.sqlite3' #variable para almacenenar el nombre de la base de datos, ../ ==> para que cree la base de datos en una carpeta anterior y no en la actual
base_dir = os.path.dirname(os.path.realpath(__file__)) #leer el directorio actual del archivo el cual es database.py

database_url = f'sqlite:///{os.path.join(base_dir,sqlite_file_name)}' #sqlite:/// ==> manera de conectarse a una base de datos, {os.path.join(base_dir,sqlite_file_name)} ==> para unir las dos variables a nuestra url

engine = create_engine(database_url, echo=True) #representará el motor de la base de datos, le pasamos la url y el echo=True para que nos muestre por consola lo que se esta realizando

Session = sessionmaker(bind=engine) #Sesion para conectarse a la base de datos, recibira el parametro del motor de la base de datos para poder conectarse

Base = declarative_base() #Se usara mas adelante