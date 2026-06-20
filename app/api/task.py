from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app.api.deps import get_db, get_current_user
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdateStatus

router = APIRouter(prefix="/tasks", tags=["Tarefas"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
        task_data: TaskCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Cria uma tarefa dentro de um projeto (Apenas se o projeto for seu)."""
    # Verifica se o projeto pertence ao usuário logado
    proj_stmt = select(Project).where(Project.id == task_data.project_id, Project.owner_id == current_user.id)
    project = db.execute(proj_stmt).scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado ou você não tem permissão para usá-lo."
        )

    new_task = Task(
        title=task_data.title,
        status=task_data.status,
        project_id=task_data.project_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/project/{project_id}", response_model=List[TaskResponse])
def list_tasks_by_project(
        project_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Lista as tarefas de um projeto específico (Apenas se o projeto for seu)."""
    # Garante o acesso ao projeto primeiro
    proj_stmt = select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    project = db.execute(proj_stmt).scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado ou acesso negado."
        )

    task_stmt = select(Task).where(Task.project_id == project_id)
    tasks = db.execute(task_stmt).scalars().all()
    return tasks

@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
        task_id: int,
        status_data: TaskUpdateStatus,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Atualiza o status de uma tarefa (Apenas se o projeto pertencer a você)."""
    # Busca a tarefa fazendo um JOIN com o projeto para checar o dono de uma vez só
    stmt = select(Task).join(Project).where(Task.id == task_id, Project.owner_id == current_user.id)
    task = db.execute(stmt).scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada ou acesso negado."
        )

    # Validação simples do status enviado
    if status_data.status not in ["pending", "in_progress", "done"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status inválido. Escolha entre: pending, in_progress ou done."
        )

    task.status = status_data.status
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Deleta uma tarefa (Apenas se o projeto pertencer a você)."""
    stmt = select(Task).join(Project).where(Task.id == task_id, Project.owner_id == current_user.id)
    task = db.execute(stmt).scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada ou acesso negado."
        )

    db.delete(task)
    db.commit()
    return None