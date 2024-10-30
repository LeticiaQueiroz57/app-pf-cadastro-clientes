from pydantic import BaseModel, Field, field_validator
from email_validator import validate_email, EmailNotValidError

class HubModel(BaseModel):
    nome: str = Field(..., description="nome não pode ser nulo")
    sobrenome: str = Field(..., description="sobrenome não pode ser nulo")
    email: str = Field(..., description="email válido é necessário")
    telefone: str = Field(..., description="telefone não pode ser nulo")
    preco: float = Field(..., description="preço deve ser positivo")

    @field_validator('preco')
    def preco_nao_ser_null(cls, value):
        if value <= 0:
            raise ValueError('O preço deve ser positivo.')
        return value
    
    @field_validator('nome', 'sobrenome', 'email', 'telefone')
    def must_not_be_empty(cls, value):
        if not value or value.strip() == "":
            raise ValueError('Campo não pode ser nulo')
        return value
    
    @field_validator('email')
    def validar_email(cls, value):
        try:
            validate_email(value)
        except EmailNotValidError as error:
            raise ValueError(str(error))
        return value
    
class Filtro(BaseModel):
    nome: str
    email: str
    phone: str