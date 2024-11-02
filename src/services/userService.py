from src.database.connection import Usuario
from src.models.userModel import userModel
from fastapi import HTTPException
from datetime import datetime
from typing import Optional


class userService:

    async def CriarDados(userModel: userModel):
        try:
            
            number = Usuario.estimated_document_count()
            if number >= 1:
                id = number + 1
            else:
                id = 1  
            hub = {
                "id": id,
                "nome": userModel.nome,
                "sobrenome": userModel.sobrenome,
                "email": userModel.email,
                "telefone": userModel.telefone,
                "datacricao": datetime.now(),
                
            }
            Usuario.insert_one(hub)
            return {"message": "Dados criados com sucesso"}
        except Exception:
            raise HTTPException(status_code=400, detail="Erro ao criar dados")
        
            
    
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
            
            if len(usuarios) == 0:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            
            return usuarios 
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))


        
    

    
    async def AtualizarCliente(user_id: int, dados_atualizados: userModel):
        try:
            cliente_existente = Usuario.find_one({"id": user_id})
            if not cliente_existente:
                raise HTTPException(status_code=404, detail="Usuario não encontrado")
            
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

            if resultado.matched_count == 0:
                raise HTTPException(status_code=400, detail="Erro ao atualizar o usuario")
            
            return {"message": "Usuario atualizado com sucesso!"}
        
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))