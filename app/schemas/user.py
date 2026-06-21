from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """Schema para validação dos dados de ENTRADA no cadastro."""
    name: str = Field(..., min_length=2, description="O nome do usuário") # 👈 Novo campo
    email: EmailStr
    password: str = Field(..., min_length=6, description="A senha deve ter no mínimo 6 caracteres")

class UserLoginResponse(BaseModel):
    """Schema para embutir os dados básicos do usuário junto ao token."""
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schema para a SAÍDA do login (o formato que o front-end vai receber)."""
    access_token: str
    token_type: str
    user: UserLoginResponse # 👈 Agora injetamos o objeto do usuário na resposta de sucesso