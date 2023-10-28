from fastapi import APIRouter
from fastapi.responses import HTMLResponse #HTMLResponse para retornar codigo html, fileresponse para retornar archivo html completo

home_router = APIRouter()

@home_router.get('/', tags=['Home']) #nuestra ruta inicial, la etiqueta (tags) sirve para  agrupar determinadas rutas de nuestra aplicación
def message():
     return HTMLResponse( #Forma de retornar un html con codigo dentro de return
         '''<h1>PelisMar</h1>
           <p>Puedes ejecutar la documentación swagger colocando en la url de la web /docs. Eso te abrira la documentacion para que puedas ver todos los metodos de nuestro servidor.</p>
         ''')
    #return FileResponse('index.html')