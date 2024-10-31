from src.database.connection import Usuario
from src.models.hubModel import HubModel
from fastapi import HTTPException
from datetime import datetime
from typing import Optional


class HubService:
    async def ListarTodos(filtro) -> list:
        try:
            if filtro ==  None:
                return list(Usuario.find())
            else:
                return list(Usuario.find({"usuariTipo": filtro.usuarioTipo}))   
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
                "datacricao": datetime.now(),
                "tipoUsraio": "user"
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
        
 

 

    async def BuscarUsuario(user_id: Optional[int] = None, nome: Optional[str] = None, email: Optional[str] = None, telefone: Optional[str] = None):
        try:
            filtro = {}
            if user_id is not None:
                filtro["id"] = user_id
            if nome is not None:
                filtro["nome"] = nome
            if email is not None:
                filtro["email"] = email
            if telefone is not None:
                filtro["telefone"] = telefone
            if not filtro:
                resultados = Usuario.find()  
            else:
                resultados = Usuario.find(filtro)  
            usuarios = []
            for resultado in resultados:
                resultado["_id"] = str(resultado["_id"])
                usuarios.append(resultado)
            return usuarios
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))


        
    

    
    async def AtualizarCliente(user_id: int, dados_atualizados: HubModel):
        try:
            resultado = Usuario.update_one(
                {"id": user_id},
                {"$set": {
                    "nome": dados_atualizados.nome,
                    "sobrenome": dados_atualizados.sobrenome,
                    "email": dados_atualizados.email,
                    "telefone": dados_atualizados.telefone,
                    "dataatualizacao": datetime.now()
                }}
            )
            if resultado.modified_count == 0:
                raise HTTPException(status_code=404, detail="Cliente não encontrado")
            return {"message": "Usuário atualizado com sucesso"}
        
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))