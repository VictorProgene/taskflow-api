from passlib.context import CryptContext

# Configura o passlib para usar o algoritmo bcrypt para o hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password: str) -> str:
    """Transforma a senha limpa em uma hash segura para o banco."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara a senha digitada no login com a hash salva no banco."""
    return pwd_context.verify(plain_password, hashed_password)