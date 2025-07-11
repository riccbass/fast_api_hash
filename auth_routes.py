from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from models import Usuario
from dependencies import pegar_sessao
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY


auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usario):

    expire_minutes = int(ACCESS_TOKEN_EXPIRE_MINUTES) if ACCESS_TOKEN_EXPIRE_MINUTES is not None else 30
    data_expiracao = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

    #normalmente se chama o id de sub
    dic_info = {"sub":id_usario, "exp":data_expiracao}

    jwt_codificado = jwt.encode(dic_info, SECRET_KEY or "batata", ALGORITHM or "HS256")

    return jwt_codificado

def autenticar_usuario(email, senha, session):

    usuario = session.query(Usuario).filter(Usuario.email == email).first() # type: ignore

    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False

    return usuario


@auth_router.get("/")
async def home():
    """
    Essa a rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "Você acessou a rota padrão de atenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)) -> dict[str, str]:
    """
    Rota para criar conta
    """

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

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)) -> dict[str, str]:
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token, "token_type": "Bearer"}
