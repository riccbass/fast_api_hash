from models import db
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from models import Usuario
from jose import jwt, JWTError

from main import SECRET_KEY, ALGORITHM, oauth2_schema

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

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):

    try:
        dic_info = jwt.decode(token, SECRET_KEY or 'batata', ALGORITHM)
        print(dic_info)
        id_usuario = int(dic_info.get('sub') or -1)
    except JWTError as erro:
        raise HTTPException(status_code=401, detail="Acesso negado, verifice a validade do token")

    #verificar se o token é valido
    #extrair o ID do usuário do TOKEN

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido")

    return usuario