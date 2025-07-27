from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, Usuario, ItemPedido


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

@order_routers.get("/list")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não possui autrização para realizar essa operação")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "Pedidos:" : pedidos
        }
    
@order_routers.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id ==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para realizar essa operação")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensagem" : "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido" : pedido.preco
    }


@order_routers.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id ==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id ==item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item do pedido não existente")
    if not usuario.admin and usuario.id != item_pedido.pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para realizar essa operação")
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensagem" : "Item removido com sucesso",
        "quantidade_itens_pedido" : len(pedido.itens),
        "pedido" : pedido
    }

@order_routers.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):

    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não possui autorização para finalizar esse pedido")
    pedido.status= "FINALIZADO"
    session.commit()
    return{
        "mensagem" : f"Pedido número {pedido.id} finalizado com sucesso",
        "pedido" : pedido
    }
    
@order_routers.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int,session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não possui autorização para visualizar esse pedido")
    return{
        "quantidade de itens do pedido": len(pedido.itens),
        "pedido": pedido
    }
    

@order_routers.get("/listar/pedidos-usuario")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não possui autrização para realizar essa operação")
    else:
        pedidos = session.query(Pedido).filter(Pedido.usuario== usuario.id).all()
        return {
            "Pedidos:" : pedidos
        }