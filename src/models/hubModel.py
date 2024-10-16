from pydantic import BaseModel

class HubModel(BaseModel):
    nome: str
    email: str
    telefone: str
    cpf: str
    endereco: str
    