from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from schemas import UsuarioSchema
from sqlalchemy.orm import Session

from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """
    Essa a rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "Você acessou a rota padrão de atenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):

    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first() # type: ignore

    if usuario:
        #já exist um usuário com esse e-mail
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        #123
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, 
                               usuario_schema.email, 
                               senha_criptografada, 
                               usuario_schema.ativo or False,
                               usuario_schema.admin or False)
        session.add(novo_usuario)
        session.commit()

        return {"mensagem":f"usuário cadastrado com sucesso {novo_usuario.email}"}


