from pydantic import BaseModel, Field

#Creacion del modelo para datos del usuario
class User(BaseModel):
    email:str = Field(default='@gmail.com', min_length=13, max_length=20)
    password:str = Field(default='1234', min_length=4, max_length=12)