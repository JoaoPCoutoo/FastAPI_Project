from fastapi import FastAPI

#Para rodar o projeto, no terminal, basta rodar o código uvicorn main:app --reload
app = FastAPI()
 
#importando s rotas necessárias após instanciar app. Importante: o nome precisa ser o mesmo definido pelo arquivo referenciado

from auth_routes import auth_routers
from order_routes import order_routers

#incluindo o uso das rotas importadas 
app.include_router(auth_routers)
app.include_router(order_routers)