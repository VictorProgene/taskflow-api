from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.database.connection import engine, Base

# IMPORTANTE: O SQLAlchemy precisa desses imports para mapear o banco
from app.models.user import User
from app.models.project import Project
from app.models.task import Task

# Cria as tabelas fisicamente no PostgreSQL se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

@app.get("/")
def root():
    return {"message": "TaskFlow API rodando com sucesso! 🚀"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        # Em vez de SELECT 1, vamos testar se a tabela 'users' realmente existe no banco
        result = db.execute(text("SELECT * FROM tasks"))
        return {
            "status": "sucesso",
            "conexao": "PostgreSQL operacional",
            "mensagem": "Tabelas validadas com sucesso no banco de dados! 🏁"
        }
    except Exception as e:
        return {
            "status": "erro",
            "mensagem": "Erro ao ler as tabelas. Elas podem não ter sido criadas.",
            "detalhes": str(e)
        }