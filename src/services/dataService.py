from src.database.connection import Usuario, Patient
from src.models.hubModel import HubModel
from fastapi import HTTPException
from datetime import datetime


async def CriarDados(hubModel: HubModel):
    try:
        id = 1
        hub = {
            "id": id,
            "nome": hubModel.nome,
            "sobrenome": hubModel.sobrenome,
            "email": hubModel.email,
            "telefone": hubModel.telefone,
            "datacricao": datetime.now()
        }
        Usuario.insert_one(hub)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
