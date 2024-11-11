from flask_openapi3 import OpenAPI, Info, Tag
from flask import request, jsonify
from model.base import Base, Session
from model.partida import Partida
from datetime import datetime

info = Info(title="EasyTruco API", version="1.0.0")
app = OpenAPI(__name__, info=info)

@app.get('/')
def hello():
    return 'Olá, Mundo!'

@app.post('/criaPartida')
def criaPartida():
    # Dados JSON
    dados = request.get_json()
    
    # Informações dos dados
    organizador = dados.get("organizador")
    local = dados.get("local")
    horario_str = dados.get("horario")  # Esperando que o horário venha como string no formato 'DD-MM-YYYY HH:MM:SS'

    # Converte o horário
    try:
        horario = datetime.strptime(horario_str, '%d-%m-%Y %H:%M:%S')
    except ValueError:
        return jsonify({"erro": "Formato de data/hora inválido. Use DD-MM-YYYY HH:MM:SS"}), 400

    # Cria uma sessão com o banco de dados
    session = Session()

    # Nova instância de Partida
    nova_partida = Partida(organizador=organizador, local=local, horario=horario)
    
    # Adiciona e confirma a nova partida no banco de dados
    session.add(nova_partida)
    session.commit()

    # Fecha a sessão
    session.close()

    # Retorna uma confirmação com o ID da nova partida
    return jsonify({"mensagem": "Partida criada com sucesso!", "id": nova_partida.id}), 201

if __name__ == '__main__':
    app.run(debug=True)
