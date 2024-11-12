from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# cria uma classe Base para o instanciamento de novos objetos/tabelas
Base = declarative_base()

# Cria o engine, que especifica o banco de dados
engine = create_engine('sqlite:///database.db')

# Cria uma fábrica de sessões
Session = sessionmaker(bind=engine)
