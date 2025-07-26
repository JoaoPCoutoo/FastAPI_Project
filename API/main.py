from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os 

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


#Para rodar o projeto, no terminal, basta rodar o código uvicorn main:app --reload
app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_schema= OAuth2PasswordBearer(tokenUrl="auth/login-form")

#importando s rotas necessárias após instanciar app. Importante: o nome precisa ser o mesmo definido pelo arquivo referenciado

from auth_routes import auth_routers
from order_routes import order_routers

#incluindo o uso das rotas importadas 
app.include_router(auth_routers)
app.include_router(order_routers)