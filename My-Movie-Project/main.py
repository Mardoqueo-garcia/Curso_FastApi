from fastapi import FastAPI #importamos el modulo

app = FastAPI() #creamos una instancia de fastapi almacenada en la variable app

#endpoint
@app.get('/') #nuestra ruta inicial
def message(): #funcion del endpoint
    return "Hola a todos desde mi servidor web"
