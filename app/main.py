from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.database.connection import engine, Base

# Import dos Roteadores da API
from app.api.auth import router as auth_router

# IMPORTANTE: O SQLAlchemy precisa desses imports para mapear o banco
from app.models.user import User
from app.models.project import Project
from app.models.task import Task

# Cria as tabelas fisicamente no PostgreSQL se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

# Inclui as rotas de autenticação sob o prefixo /auth
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "TaskFlow API rodando com sucesso! 🚀"}