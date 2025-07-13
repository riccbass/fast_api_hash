from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str 
    senha: str 
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True #se não passar, vem como dicionário

class PedidoSchema(BaseModel):
    id_usuario: int

    class Config:
        from_attributes = True #se não passar, vem como dicionário

class LoginSchema(BaseModel):

    email: str
    senha: str

    class Config:
        from_atributes = True #se não passar, vem como dicionário

class ItemPedidoSchema(BaseModel):

    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    class Config:
        from_atributes = True #se não passar, vem como dicionário

