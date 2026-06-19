from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings


def create_access_token(data: dict) -> str:
    """Gera um token JWT assinado digitalmente."""
    to_encode = data.copy()

    # Define o tempo de expiração do token (60 minutos)
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Adiciona o campo 'exp' (expiration) no payload do token
    to_encode.update({"exp": expire})

    # Codifica os dados usando a nossa chave secreta e o algoritmo definidos no .env
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt