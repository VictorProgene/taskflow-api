from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.connection import SessionLocal  # Mantendo o seu import
from app.models.user import User
from app.core.config import settings

# 1. Informa ao FastAPI que o token deve ser buscado no endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# O seu gerenciador de banco de dados continua aqui, intacto
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 2. Nova função: O segurança das suas rotas protegidas
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Intercepta a requisição, valida o Token JWT e retorna o usuário logado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o Token usando a SECRET_KEY do seu settings
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Busca o usuário no banco usando o ID que veio dentro do token
    stmt = select(User).where(User.id == int(user_id))
    user = db.execute(stmt).scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user