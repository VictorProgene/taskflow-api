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
        # Executa um comando simples SQL para testar a comunicação
        result = db.execute(text("SELECT 1"))
        row = result.fetchone()
        return {
            "status": "sucesso",
            "conexao": "PostgreSQL operacional",
            "resultado": row[0] if row else None
        }
    except Exception as e:
        # Se der erro, ele não vai dar apenas "Internal Server Error", ele vai te dizer o porquê
        return {
            "status": "erro",
            "mensagem": "Não foi possível conectar ao banco de dados.",
            "detalhes": str(e)
        }