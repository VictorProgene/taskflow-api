from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
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
    stmt = select(User).where(User.email == user_data.email)
    existing_user = db.execute(stmt).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado."
        )

    hashed_pwd = generate_password_hash(user_data.password)

    # 👈 Salvando o campo name mapeado do schema de entrada
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário cadastrado com sucesso!", "id": new_user.id}


@router.post("/login", response_model=Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Rota de login que valida as credenciais e retorna o Token JWT."""
    stmt = select(User).where(User.email == credentials.username)
    user = db.execute(stmt).scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    # 👈 Retornamos o token acoplado aos dados do modelo de usuário de forma aninhada
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }