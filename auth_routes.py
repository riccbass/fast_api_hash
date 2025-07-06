from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def autenticar():
    """
    Essa a rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "Você acessou a rota padrão de atenticação", "autenticado": False}


# "python.formatting.autopep8Args": ["--ignore", "E402"]
