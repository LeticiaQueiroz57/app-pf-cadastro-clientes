from pydantic import BaseModel, Field, field_validator, model_validator
from email_validator import validate_email, EmailNotValidError

class userModel(BaseModel):
    nome: str = Field(..., description="nome não pode ser nulo")
    sobrenome: str = Field(..., description="sobrenome não pode ser nulo")
    email: str = Field(..., description="email válido é necessário")
    telefone: str = Field(..., description="telefone não pode ser nulo")

    @model_validator(mode="before")
    def verificar_email(cls, values):
        email = values.get('email')
        try:
            validate_email(email)
        except EmailNotValidError as e:
            raise ValueError("O email contém caracteres inválidos")  
        return values

    @model_validator(mode="before")
    def must_not_be_empty(cls, values):
        for field in ['nome', 'sobrenome', 'telefone']:
            if not values.get(field) or values.get(field).strip() == "":
                raise ValueError(f'{field} não pode ser nulo')
        return values
