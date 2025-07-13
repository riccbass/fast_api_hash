from fastapi import APIRouter, Depends, HTTPException
from dependencies import pegar_sessao, verificar_token
from sqlalchemy.orm import Session
from schemas import PedidoSchema
from models import Pedido, Usuario

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

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

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, 
                          session: Session = Depends(pegar_sessao),
                          usuario: Usuario = Depends(verificar_token)):
    
    #usuario.admin = True
    #usuario.id = pedido.usuario

    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if not usuario.admin or usuario.id != pedido.usuario: # type: ignore
        raise HTTPException(status_code=401, detail="Voce não tem autorização para fazer essa modificação")        

    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido número: {pedido.id} cancelado com sucesso", #passando o campo, 
        #obriga o modelo a importar todos os campos
        "pedido": pedido
    }


