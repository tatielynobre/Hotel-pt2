from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import logging 
import os

#carregando as variaveis
load_dotenv()

#Configurando o logger
logging.basicConfig()
logging.getLogger("").setLevel(logging.INFO)

engine = create_engine(os.getenv(""))

#criando
#inicializando
def create_db()-> None:
    SQLModel.metadata.create_all(engine)

def get_session()-> Session:
    return Session(engine)

