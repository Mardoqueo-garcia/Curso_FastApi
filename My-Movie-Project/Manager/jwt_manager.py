from jwt import encode, decode

#funcion para poder generar ese token
def create_token(data : dict) -> str:
    token : str = encode(payload=data, key='M4rd0qu30_G4rc14', algorithm='HS256')
    return token

#funcion para validar token
def validate_token(token : str) -> dict: #retornara un diccionario
    data: dict = decode(token, key='M4rd0qu30_G4rc14', algorithms=['HS256']) #recibe el token, la clave y el algoritmo solo que seria de tipo lista. Obtendremos los datos que el usuario utilizo para generar ese token
    return data