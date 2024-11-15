from flask_openapi3 import OpenAPI, Info, Tag
from flask import request, jsonify, redirect
from model.base import Base, Session, engine
from model.partida import Partida
from model.usuario import Usuario
from datetime import datetime
from schemas.partida import PartidaSchema
from schemas.usuario import UsuarioSchema

# Cria as tabelas no banco de dados
Base.metadata.create_all(engine)

info = Info(title="EasyTruco API", version="1.0.0")
app = OpenAPI(__name__, info=info)

@app.get('/')
def hello():
    return 'Olá, Mundo!'

@app.post('/criaPartida')
def criaPartida(form: PartidaSchema):

    session = Session()

    organizador = form.organizador
    local = form.local
    horario = form.horario

    if not organizador or not local or not horario:
        session.close()
        return jsonify({"mensagem": "Preencha todos os campos!"}), 400
    
    # Verifica se o horário está no passado
    if horario < datetime.now():
        session.close()
        return jsonify({"mensagem": "O horário da partida deve ser no futuro!"}), 400

    novaPartida = Partida(organizador=organizador, local=local, horario=horario)
    
    session.add(novaPartida)
    session.commit()

    session.close()
    return jsonify({"mensagem": "Partida criada com sucesso!", "id": novaPartida.id}), 201

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
