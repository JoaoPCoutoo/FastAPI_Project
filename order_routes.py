from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema
from models import Pedido, Usuario


#definindo a rota de autenticação da aplicação
order_routers = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

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

@order_routers.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):

    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não possui autorização para cancelar esse pedido")
    pedido.status= "CANCELADO"
    session.commit()
    return{
        "mensagem" : f"Pedido número {pedido.id} cancelado com sucesso",
        "pedido" : pedido
    }
