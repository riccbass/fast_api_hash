from fastapi import APIRouter, Depends
from dependencies import pegar_sessao
from sqlalchemy.orm import Session
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
    """
    Essa a rota padrão de pedidos do nosso sistema.
    """
    return {"mensagem":"sucesso"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):

    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()

    return {"mensagem":f"Pedido criado com sucesso. ID do pedido {novo_pedido.id}"}