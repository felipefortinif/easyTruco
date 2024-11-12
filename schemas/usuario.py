from pydantic import BaseModel

class UsuarioSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = "Nome Completo dos Santos"
    email: str = "email@gmail.com"
    senha: str = "senha123" 