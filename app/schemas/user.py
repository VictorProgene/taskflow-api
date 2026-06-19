from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """Schema para validação dos dados de ENTRADA no cadastro."""
    email: EmailStr
    password: str = Field(..., min_length=6, description="A senha deve ter no mínimo 6 caracteres")

class Token(BaseModel):
    """Schema para a SAÍDA do login (o formato que o front-end vai receber)."""
    access_token: str
    token_type: str