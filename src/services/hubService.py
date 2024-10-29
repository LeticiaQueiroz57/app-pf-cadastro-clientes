from src.database.connection import Usuario
from src.models.hubModel import HubModel
from fastapi import HTTPException
from datetime import datetime

class HubService:
    async def ListarTodos() -> list:
        try:
            return list(Usuario.find())
        except Exception as error:
            raise HTTPException(400, detail=error)
    
    async def CriarDados(hubModel: HubModel):
        try:
            
            number = Usuario.estimated_document_count()
            if number >= 1:
                id = number + 1
            else:
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
            raise HTTPException(400, detail=error)
            
    
    async def RemoverUsuario(user_id: int):
        try:
            resultado = Usuario.delete_one({"id": user_id})
            if resultado.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            return {"message": "Usuário removido com sucesso"}
        except Exception as error:
            raise HTTPException(400, detail=str(error))
        
    async def  BuscarUsuario(user_id: int):
        try:
            resultado = Usuario.find_one({"id": user_id})
            if resultado is None:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            resultado["_id"] = str(resultado["_id"])
            return resultado
        except Exception as error:
            raise HTTPException(400, detail=str(error))
        
    