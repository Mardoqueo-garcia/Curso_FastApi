import json #para usar el formato de lectura json
file = open("data/datas.json") #abrimos el archivo
data = json.load(file) #cargamos ese archivo en la variable data
file.close #cerramos el archivo