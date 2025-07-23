from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido


#definindo a rota de autenticação da aplicação
order_routers = APIRouter(prefix="/pedidos", tags=["pedidos"])

#definindo rota padrão 
#nesse caso, a rota seria dominio/order/
#utilização de uma função assíncrona async, e o restante é uma função comum em Python
#nesse caso, é uma requisição do tipo get 
@order_routers.get("/")
async def pedidos ():
    """
    Essa é a rota padrão de pedidos do sistema
    """
    return {"mensagem": "voce acessou a rota de pedidos!"}

@order_routers.post("/pedidos")
async def criar_pedido (pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao) ):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return{"mensagem": f"Pedido criado com sucesso! Id do pedido: {novo_pedido.id}"}