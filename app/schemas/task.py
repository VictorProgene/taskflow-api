from pydantic import BaseModel
from typing import Optional

# Mini schema do Projeto para ser incluído dentro da resposta da Tarefa
class ProjectMinResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    status: Optional[str] = "pending"  # Valores: pending, in_progress, done
    priority: Optional[str] = "medium"  # Nova Coluna! Valores: low, medium, high

class TaskCreate(TaskBase):
    project_id: int

class TaskResponse(TaskBase):
    id: int
    project_id: int
    # Mágica: Aqui o FastAPI vai olhar o relacionamento 'project' do model
    # e preencher automaticamente com o id e name do projeto!
    project: Optional[ProjectMinResponse] = None

    class Config:
        from_attributes = True

class TaskUpdateStatus(BaseModel):
    status: str  # pending, in_progress, done