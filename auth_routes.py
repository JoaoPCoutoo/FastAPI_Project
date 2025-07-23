from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session

#definindo a rota de autenticação da aplicação
auth_routers = APIRouter(prefix="/auth", tags= ["auth"])

def criar_token(id_usuario):
    token = f"kwjfn3weubn4fjen{id_usuario}"
    return token

#definição da rota padrão 
@auth_routers.get("/")
async def home ():
    """
    Essa é a rota padrão de autenticação do sistema
    """
    return{"mensagem": "Voce entrou na rota de autenticação", "autenticado": False}

@auth_routers.post("/criar_conta")
async def criar_conta (usuario_schema:UsuarioSchema, session:Session= Depends(pegar_sessao)):
    #Busca usuário
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        #um usuário já está cadastrado com esse email
        raise HTTPException(status_code=400, detail="E-mail de usuário já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuário cadastrado com sucesso {usuario_schema.email}"}
    
@auth_routers.post("/login")
async def login(login_schema: LoginSchema, session:Session= Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    else:
        acess_token = criar_token(usuario.id)
        return {
            "acess_token": acess_token,
            "token_type": "Bearer"
                }