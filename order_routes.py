from fastapi import APIRouter

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
