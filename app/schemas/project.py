from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # Permite que o Pydantic leia modelos do SQLAlchemy