from pydantic import BaseModel
from datetime import datetime

class PartidaSchema(BaseModel):
    """ Define como uma nova partida a ser inserida deve ser representada """
    organizador: str = "Nome do Organizador"
    local: str = "Local da Partida"
    horario: datetime = datetime.now()

