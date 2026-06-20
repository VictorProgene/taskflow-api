from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse # Se preferir manter simples, use JSONResponse
from sqlalchemy.exc import SQLAlchemyError  # Captura qualquer erro de banco de dados
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.database.connection import engine, Base

# Import dos Roteadores da API
from app.api.deps import get_current_user
from app.api.auth import router as auth_router
from app.api.project import router as project_router
from app.api.task import router as task_router

# IMPORTANTE: O SQLAlchemy precisa desses imports para mapear o banco
from app.models.user import User
from app.models.project import Project
from app.models.task import Task

# Cria as tabelas fisicamente no PostgreSQL se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

@app.exception_handler(SQLAlchemyError)
def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Se houver qualquer erro de banco de dados (ex: perda de conexão, dados corrompidos),
    este interceptador captura o erro e envia uma resposta amigável para o cliente.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Ocorreu um erro interno de comunicação com o banco de dados. Tente novamente mais tarde."}
    )

# Inclui as rotas de autenticação sob o prefixo /auth
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(task_router)

@app.get("/")
def root():
    return {"message": "TaskFlow API rodando com sucesso! 🚀"}

# ... seus outros imports ...
from app.api.deps import get_current_user
from app.models.user import User

# ... configuração do app e include_router ...

@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    """Rota protegida que só responde se um Token JWT válido for enviado."""
    return {
        "message": "Você está autenticado!",
        "user_email": current_user.email,
        "user_id": current_user.id
    }