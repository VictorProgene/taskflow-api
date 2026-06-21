from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) # 👈 Nova coluna adicionada
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relacionamento: Um usuário pode ter muitos projetos
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")