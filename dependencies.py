from models import db
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    session = None #isso é para garantir que vai existir session
    #se não tiver, e sesse erro no sessionmaker, não ia ter session ainda
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        if session is not None:
            session.close()