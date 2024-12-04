from flask_openapi3 import OpenAPI, Info, Tag
from flask import request, jsonify, redirect, Flask, render_template, url_for, flash
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

# Configuração da chave secreta para usar flash e sessões
app.config['SECRET_KEY'] = 'CHAVE_FLASH_REDIRECIONAR'

@app.get('/')
def home():
    return render_template('index.html')

@app.route('/listagem_partidas')
def listagem_partidas():
    session = Session()
    usuario_id = 1
    partidas = session.query(Partida).all()
    session.close()

    return render_template('listagem_partidas.html', partidas=partidas, usuario_id=usuario_id)

@app.route('/cadastro')
def index():
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    mensagem = None
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('password')

        session = Session()
        usuario = session.query(Usuario).filter(Usuario.email == email).first()

        if usuario and usuario.senha == senha:
            return redirect('listagem_partidas')

        else:
            mensagem = 'Usuário ou senha inválidos!'  
    return render_template('login.html', mensagem=mensagem)

@app.route('/cadastrar_usuario', methods=['POST'])
def criaUsuario():
    session = Session()

    try:
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not email or not senha:
            return jsonify({"mensagem": "Preencha todos os campos!"}), 400

        if session.query(Usuario).filter(Usuario.email == email).first():
            return jsonify({"mensagem": "Este email já está cadastrado!"}), 400

        if not validarSenha(senha):
            return jsonify({"mensagem": "Senha deve ter pelo menos 8 caracteres e conter letras e números!"}), 400

        novoUsuario = Usuario(nome=nome, email=email, senha=senha)

        session.add(novoUsuario)
        session.commit()

        return jsonify({"mensagem": "Usuário criado com sucesso!", "id": novoUsuario.id}), 201

    except Exception as e:
        session.rollback()
        return jsonify({"mensagem": f"Erro ao criar o usuário: {str(e)}"}), 500

    finally:
        session.close()

@app.route('/cadastrar_partida')
def cadastrar_partida():
    return render_template('cadastrar_partida.html')

@app.post('/criaPartida')
def criaPartida():
    session = Session()

    try:
        organizador = request.form.get('organizador')
        local = request.form.get('local')
        horario_str = request.form.get('horario')

        if not organizador or not local or not horario_str:
            return jsonify({"mensagem": "Preencha todos os campos!"}), 400

        # Converte o horário para datetime
        try:
            horario = datetime.fromisoformat(horario_str)
        except ValueError:
            return jsonify({"mensagem": "Formato de horário inválido!"}), 400

        # Verifica se o horário está no passado
        if horario < datetime.now():
            return jsonify({"mensagem": "O horário da partida deve ser no futuro!"}), 400

        # Cria uma nova partida
        novaPartida = Partida(organizador=organizador, local=local, horario=horario)

        session.add(novaPartida)
        session.commit()

        return jsonify({"mensagem": "Partida criada com sucesso!", "id": novaPartida.id}), 201

    except Exception as e:
        session.rollback()
        return jsonify({"mensagem": f"Erro ao criar a partida: {str(e)}"}), 500

    finally:
        session.close()

@app.route('/entrar_partida/<int:id>', methods=['POST'])
def entrar_partida(id):
    session = Session()

    try:
        # Obtém o usuário que está tentando entrar
        usuario_id = 1  # Aqui você pode pegar o id do usuário logado, por exemplo

        # Busca a partida pelo ID
        partida = session.query(Partida).filter(Partida.id == id).first()

        if not partida:
            flash("Partida não encontrada!", "error")
            return redirect(url_for('listagem_partidas'))

        # Verifica se a partida tem vagas (menos de 4 jogadores)
        jogadores = partida.jogadores.split(',')
        if len(jogadores) >= 4:
            flash("Partida cheia!", "error")
            return redirect(url_for('listagem_partidas'))

        # Adiciona o usuário à lista de jogadores
        jogadores.append(str(usuario_id))  # Adiciona o id do jogador à lista
        partida.jogadores = ','.join(jogadores)  # Atualiza a lista de jogadores

        # Commit na transação
        session.commit()

        flash("Você entrou na partida com sucesso!", "success")
        return redirect(url_for('listagem_partidas'))

    except Exception as e:
        session.rollback()
        flash(f"Erro ao entrar na partida: {str(e)}", "error")
        return redirect(url_for('listagem_partidas'))

    finally:
        session.close()

@app.route('/sair_partida/<int:id>', methods=['POST'])
def sair_partida(id):
    session = Session()

    try:
        # Obtém o usuário que está tentando sair
        usuario_id = 1  # Aqui você pode pegar o id do usuário logado, por exemplo

        # Busca a partida pelo ID
        partida = session.query(Partida).filter(Partida.id == id).first()

        if not partida:
            flash("Partida não encontrada!", "error")
            return redirect(url_for('listagem_partidas'))

        # Verifica se o usuário está na partida
        jogadores = partida.jogadores.split(',')
        if str(usuario_id) not in jogadores:
            flash("Você não está na partida!", "info")
            return redirect(url_for('listagem_partidas'))

        # Remove o jogador da lista
        jogadores = [j for j in jogadores if j != str(usuario_id)]
        partida.jogadores = ','.join(jogadores)  # Atualiza a lista de jogadores

        # Commit na transação
        session.commit()

        flash("Você saiu da partida com sucesso!", "success")
        return redirect(url_for('listagem_partidas'))

    except Exception as e:
        session.rollback()
        flash(f"Erro ao sair da partida: {str(e)}", "error")
        return redirect(url_for('listagem_partidas'))

    finally:
        session.close()

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
