from pydantic import BaseModel, Field, field_validator, model_validator
from email_validator import validate_email, EmailNotValidError
from typing import Optional
class userModel(BaseModel):
    nome: Optional[str] = Field(None, description="nome não pode ser nulo")
    sobrenome: Optional[str] = Field(None, description="sobrenome não pode ser nulo")
    email: Optional[str] = Field(None, description="email válido é necessário")
    telefone: Optional[str] = Field(None, description="telefone não pode ser nulo")
    

    
