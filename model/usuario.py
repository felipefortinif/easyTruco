from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model.base import Base

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column('pk_usuario', Integer, primary_key=True)
    nome = Column(String(100))
    email = Column(String(100))
    senha = Column(String(100))

    def __init__(self, nome: str, email: str, senha: str):
        self.nome = nome
        self.email = email
        self.senha = senha