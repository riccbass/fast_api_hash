from fastapi import APIRouter, Depends
from models import Usuario
from dependencies import pegar_sessao

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """
    Essa a rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "Você acessou a rota padrão de atenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(email: str, senha: str, nome: str, session = Depends(pegar_sessao)):

    usuario = session.query(Usuario).filter(Usuario.email == email).first() # type: ignore

    if usuario:
        #já exist um usuário com esse e-mail
        return {"mensagem": "já existe um usuário com esse e-mail"}
    else:
        novo_usuario = Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()

        return {"mensagem":"usuário cadastrado com sucesso"}


