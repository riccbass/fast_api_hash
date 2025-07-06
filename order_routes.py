from fastapi import APIRouter

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
    """
    Essa a rota padrão de pedidos do nosso sistema.
    """
    return {"mensagem":"sucesso"}