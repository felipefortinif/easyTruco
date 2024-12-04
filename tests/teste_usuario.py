import unittest
from unittest.mock import patch, MagicMock
from model.usuario import Usuario

class TestUsuario(unittest.TestCase):

    @patch('sqlalchemy.orm.session.Session.query')
    def test_email_ja_cadastrado(self, mock_query):
        # Simula um email já existente no banco de dados
        mock_query.return_value.filter_by.return_value.first.return_value = MagicMock()

        # Simula a lógica de verificação de email
        email_existe = mock_query.return_value.filter_by(email="teste@example.com").first() is not None

        # Verifica se o email já está cadastrado
        self.assertTrue(email_existe)

    def test_senha_curta(self):
        # Tenta criar um usuário com uma senha curta
        usuario = Usuario(nome="Teste", email="teste@example.com", senha="123")

        # Verifica se a senha é considerada curta
        self.assertTrue(len(usuario.senha) < 6)

    def test_senha_sem_numero(self):
        # Tenta criar um usuário com uma senha sem número
        usuario = Usuario(nome="Teste", email="teste@example.com", senha="senha")

        # Verifica se a senha não contém números
        self.assertFalse(any(char.isdigit() for char in usuario.senha))

if __name__ == '__main__':
    unittest.main()
