from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app.api.deps import get_db, get_current_user
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projetos"])

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Rota protegida!
):
    """Cria um novo projeto atrelado ao usuário logado."""
    new_project = Project(name=project_data.name, owner_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/", response_model=List[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Rota protegida!
):
    """Lista APENAS os projetos que pertencem ao usuário logado."""
    stmt = select(Project).where(Project.owner_id == current_user.id)
    projects = db.execute(stmt).scalars().all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
        project_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Busca um projeto específico por ID (Apenas se pertencer ao usuário logado)."""
    stmt = select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    project = db.execute(stmt).scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado ou você não tem permissão para acessá-lo."
        )
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
        project_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Deleta um projeto por ID (Apenas se pertencer ao usuário logado)."""
    stmt = select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    project = db.execute(stmt).scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado ou você não tem permissão para acessá-lo."
        )

    db.delete(project)
    db.commit()
    return None  # HTTP 204 não retorna corpo de resposta