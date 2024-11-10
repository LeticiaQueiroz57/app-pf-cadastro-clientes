from src.database.connection import Usuario
from src.models.userModel import userModel
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
import re

class userService:

    async def CriarDados(userModel: userModel):
        try:
            if len(userModel.email) > 20:
                raise HTTPException(status_code=400, detail="O email não pode ter mais de 20 caracteres")
                
            if len(userModel.telefone) > 11:
                raise HTTPException(status_code=400, detail="O telefone não pode ter mais de 11 caracteres")
                
            email_duplicado = Usuario.find_one({"email": userModel.email.lower()})
            if email_duplicado:
                raise HTTPException(status_code=400, detail="Já existe um usuário com este email")

            if not re.fullmatch(r'\d+', userModel.telefone):
                raise HTTPException(status_code=400, detail="O número de telefone deve conter apenas números")
            
            if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", userModel.email):
                raise HTTPException(status_code=422, detail="O email contém caracteres inválidos")

            telefone_duplicado = Usuario.find_one({"telefone": userModel.telefone})
            if telefone_duplicado:
                raise HTTPException(status_code=400, detail="Já existe um usuário com este telefone")

            ultimo_usuario = Usuario.find_one(sort=[("id", -1)])
            id = ultimo_usuario["id"] + 1 if ultimo_usuario else 1

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
        except HTTPException as error:
            raise error
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
                filtro["email"] = email.lower()
            if telefone is not None:
                filtro["telefone"] = re.sub(r'\D', '', telefone)
            resultados = Usuario.find(filtro) if filtro else Usuario.find()
            usuarios = []
            for resultado in resultados:
                resultado["_id"] = str(resultado["_id"])
                usuarios.append(resultado)

            if not usuarios:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")

            return usuarios
        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))

    async def AtualizarCliente(user_id: int, dados_atualizados: userModel):
        try:
            
            if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", dados_atualizados.email):
                raise HTTPException(status_code=422, detail="O email contém caracteres inválidos")

            cliente_existente = Usuario.find_one({"id": user_id})
            if not cliente_existente:
                raise HTTPException(status_code=404, detail="Usuario não encontrado")
            
            email_duplicado = Usuario.find_one({"email": dados_atualizados.email, "id": {"$ne": user_id}})
            if email_duplicado:
                raise HTTPException(status_code=422, detail="Já existe um usuário com este email")

            telefone_duplicado = Usuario.find_one({"telefone": dados_atualizados.telefone, "id": {"$ne": user_id}})
            if telefone_duplicado:
                raise HTTPException(status_code=422, detail="Já existe um usuário com este telefone")


            resultado = Usuario.update_one(
                {"id": user_id},
                {"$set": {
                    "nome": dados_atualizados.nome,
                    "sobrenome": dados_atualizados.sobrenome,
                    "email": dados_atualizados.email.lower(),
                    "telefone": dados_atualizados.telefone,
                    "dataatualizacao": datetime.now()
                }}
            )
            if resultado.matched_count == 0:
                raise HTTPException(status_code=422, detail="Erro ao atualizar o usuario")
            
            return {"message": "Usuario atualizado com sucesso!"}

        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))
