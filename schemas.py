from pydantic import BaseModel
from typing import Optional

#schemas são as classes que vão padronizar o formato das informações recebidas

class UsuarioSchema (BaseModel):
    nome: str
    email: str 
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True

class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email:str
    senha: str

    class Config:
        from_attributes = True