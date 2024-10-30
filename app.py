from flask_openapi3 import OpenAPI, Info, Tag
# from model import Base, Partida, Session

from model.base import Base
from model.partida import Partida

info = Info(title="EasyTruco API", version="1.0.0")
app = OpenAPI(__name__, info=info)

@app.get('/')
def hello():
    return 'Olá, Mundo!'

@app.post('/criaPartida')
def criaPartida():

    return 'Cria partida!'

if __name__ == '__main__':
    app.run(debug=True)
