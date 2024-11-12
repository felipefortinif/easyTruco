from flask_openapi3 import OpenAPI, Info, Tag
from flask import request, jsonify, redirect
from model.base import Base, Session, engine
from model.partida import Partida
from model.usuario import Usuario
from datetime import datetime
from schemas.usuario import UsuarioSchema

# Cria as tabelas no banco de dados
Base.metadata.create_all(engine)

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

@app.post('/criaUsuario')
def criaUsuario(form: UsuarioSchema):

    session = Session()

    nome = form.nome
    email = form.email
    senha = str(form.senha)

    if not nome or not email or not senha:
        session.close()
        return jsonify({"mensagem": "Preencha todos os campos!"}), 400
    
    emailExiste = session.query(Usuario).filter(Usuario.email == email).first() is not None
    if emailExiste:
        session.close()
        return jsonify({"mensagem": "Este email já está cadastrado!"}), 400
    
    ehSenhaValida = validarSenha(senha)
    if not ehSenhaValida:
        session.close()
        return jsonify({"mensagem": "Senha inválida! Deve conter pelo menos 8 caracteres, letras e números!"}), 400

    novoUsuario = Usuario(nome=nome, email=email, senha=senha)
    
    session.add(novoUsuario)
    session.commit()

    session.close()
    return jsonify({"mensagem": "Usuário criado com sucesso!", "id": novoUsuario.id}), 201

def validarSenha(senha: str):
    if len(senha) < 8:
        return False
    
    possui_letra = any(char.isalpha() for char in senha)
    possui_numero = any(char.isdigit() for char in senha)
    
    if not possui_letra or not possui_numero:
        return False
    
    return True

if __name__ == '__main__':
    app.run(debug=True)
