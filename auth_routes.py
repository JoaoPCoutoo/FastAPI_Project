from fastapi import APIRouter

#definindo a rota de autenticação da aplicação
auth_routers = APIRouter(prefix="/auth", tags= ["auth"])

#definição da rota padrão 
@auth_routers.get("/")
async def autenticar ():
    """
    Essa é a rota padrão de autenticação do sistema
    """
    return{"mensagem": "Voce entrou na rota de autenticação", "autenticado": False}