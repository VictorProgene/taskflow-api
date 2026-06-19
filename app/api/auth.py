from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate, Token
from app.core.security import generate_password_hash, verify_password
from app.core.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Rota para cadastrar um novo usuário de forma segura."""
    # Verifica se o e-mail já está cadastrado no banco
    stmt = select(User).where(User.email == user_data.email)
    existing_user = db.execute(stmt).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado."
        )

    # Cria a hash da senha antes de salvar
    hashed_pwd = generate_password_hash(user_data.password)

    # Instancia o novo usuário no modelo do SQLAlchemy
    new_user = User(email=user_data.email, hashed_password=hashed_pwd)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário cadastrado com sucesso!", "id": new_user.id}


@router.post("/login", response_model=Token)
def login(credentials: UserCreate, db: Session = Depends(get_db)):
    """Rota de login que valida as credenciais e retorna o Token JWT."""
    # Busca o usuário pelo e-mail
    stmt = select(User).where(User.email == credentials.email)
    user = db.execute(stmt).scalar_one_or_none()

    # Se o usuário não existir ou a senha estiver incorreta
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Se tudo estiver certo, gera o Token passando o ID do usuário no payload
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}