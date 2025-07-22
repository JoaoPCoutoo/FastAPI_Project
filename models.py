from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
#from sqlalchemy_utils.types import ChoiceType

#quando fizer deploy do projeto, colocar aqui o link para onecção com o banco de dados
db = create_engine("sqlite:///banco.db")

#cria a base do banco de dados
Base = declarative_base()

# cria as classes/tabelas do banco

# usuário
class Usuario (Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key= True, autoincrement= True)
    nome = Column ("nome", String)
    email = Column ("email", String, nullable= False)
    senha = Column ("senha", String)
    ativo = Column ("ativo", Boolean)
    admin = Column ("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email= email
        self.senha = senha 
        self.ativo = ativo
        self.admin = admin


# pedido

class Pedido (Base):
    __tablename__ = "pedidos"

 #   STATUS_PEDIDOS = (
 #       ("PENDENTE", "PENDENTE"),
 #      ("CANCELADO", "CANCELADO"),
 #      ("FINALIZADO", "FINALIZADO")
 #  )

    id= Column("id", Integer, primary_key= True, autoincrement= True)
    #status= Column("status", ChoiceType(choices=STATUS_PEDIDOS)) #pendente, cancelado, finalizado
    status= Column("status", String)
    usuario= Column("usuario", ForeignKey("usuarios.id"))
    preco= Column("preco", Float)
    #itens=

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status

# itens pedido

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key= True, autoincrement= True)
    quantidade = Column("quantidade", Integer)
    sabor= Column("sabor", String)
    tamanho= Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade 
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

#executa a criação dos metadados do seu banco (cria efetivamente o banco de dados)
