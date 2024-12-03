from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model.base import Base

class Partida(Base):
    __tablename__ = 'partida'

    id = Column('pk_partida', Integer, primary_key=True)
    organizador = Column(String(100))
    local = Column(String(100))
    horario = Column(DateTime)
    jogadores = Column(Text)

    def __init__(self, organizador: str, local: str, horario: datetime):
        self.organizador = organizador
        self.local = local
        self.horario = horario
        self.jogadores = organizador