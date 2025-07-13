from fastapi import APIRouter, Depends, HTTPException
from dependencies import pegar_sessao, verificar_token
from sqlalchemy.orm import Session
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, Usuario, ItemPedido

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


@order_router.get("/listar")
async def listar_pedidos(n_pedidos: int = 10,
                         session: Session = Depends(pegar_sessao),
                         usuario: Usuario = Depends(verificar_token)):
    
    if not usuario.admin: # type: ignore
        raise HTTPException(status_code=401, detail="Voce não tem autorização para fazer essa modificação")   
    else:
        pedidos = session.query(Pedido).order_by(Pedido.id.desc()).limit(n_pedidos).all()
        return {
            "pedidos":pedidos
        }
        

@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int,
                                item_pedidos_schema: ItemPedidoSchema,
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido inexistente") 
    if not usuario.admin and usuario.id != pedido.usuario: # type: ignore
        raise HTTPException(status_code=401, detail="Voce não tem autorização para fazer essa modificação")   
    
    item_pedido = ItemPedido(item_pedidos_schema.quantidade, item_pedidos_schema.sabor,
                             item_pedidos_schema.tamanho, item_pedidos_schema.preco_unitario,
                             id_pedido)
    

    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()

    return {
        "mensagem":"Item criado com sucesso",
        "item_id":item_pedido.id,
        "preco_pedido": pedido.preco,

    }
