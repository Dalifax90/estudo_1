from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None



class UsuarioResponse(UsuarioBase):
    id: int
    # Permite converter direto do objeto SQLAlchemy (antigo orm_mode)
    model_config = ConfigDict(from_attributes=True)