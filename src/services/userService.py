from src.database.connection import Usuario
from src.models.userModel import userModel
from fastapi import HTTPException
from datetime import datetime
from typing import Optional


class userService:

    async def CriarDados(userModel: userModel):
        try:
            
            email_duplicado = Usuario.find_one({"email": userModel.email})
            if email_duplicado:
                raise HTTPException(status_code=400, detail="Já existe um usuário com este email")

            
            telefone_duplicado = Usuario.find_one({"telefone": userModel.telefone})
            if telefone_duplicado:
                raise HTTPException(status_code=400, detail="Já existe um usuário com este telefone")

            ultimo_usuario = Usuario.find_one(sort=[("id", -1)])
            if ultimo_usuario:
                id = ultimo_usuario["id"] + 1
            else:
                id = 1

            hub = {
                "id": id,
                "nome": userModel.nome,
                "sobrenome": userModel.sobrenome,
                 "email": userModel.email.lower(),
                "telefone": userModel.telefone,
                "datacricao": datetime.now(),
                }

            Usuario.insert_one(hub)
            return {"message": "Dados criados com sucesso"}
        except Exception as error:
            raise HTTPException(status_code=400, detail=f"Erro ao criar dados: {str(error)}")

        
            
    
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


        
    

    
    from fastapi import HTTPException
from datetime import datetime

async def AtualizarCliente(user_id: int, dados_atualizados: userModel):
    try:
        # Verifica se o usuário existe
        cliente_existente = Usuario.find_one({"id": user_id})
        if not cliente_existente:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Verifica se o email já está em uso por outro usuário
        email_duplicado = Usuario.find_one({"email": dados_atualizados.email, "id": {"$ne": user_id}})
        if email_duplicado:
            raise HTTPException(status_code=400, detail="Já existe um usuário com este email")

        # Verifica se o telefone já está em uso por outro usuário
        telefone_duplicado = Usuario.find_one({"telefone": dados_atualizados.telefone, "id": {"$ne": user_id}})
        if telefone_duplicado:
            raise HTTPException(status_code=400, detail="Já existe um usuário com este telefone")

        # Atualiza somente os campos preenchidos
        atualazar = {}

        if dados_atualizados.nome:
            atualazar["nome"] = dados_atualizados.nome

        if dados_atualizados.sobrenome:
            atualazar["sobrenome"] = dados_atualizados.sobrenome

        if dados_atualizados.email:
            atualazar["email"] = dados_atualizados.email

        if dados_atualizados.telefone:
            atualazar["telefone"] = dados_atualizados.telefone

        # Define a data de atualização
        atualazar["dateatualizacao"] = datetime.now()

        # Executa a atualização se houver dados a atualizar
        if atualazar:
            Usuario.update_one(
                { "id": user_id },
                { 
                    "$set": atualazar
                }
            )
        else:
            raise HTTPException(400, detail="Nenhum campo foi preenchido para atualização.")
    except Exception as error:
        raise HTTPException(400, detail=str(error))
