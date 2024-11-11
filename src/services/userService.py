from src.database.connection import Usuario
from src.models.userModel import userModel
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
import re

class userService:

    async def CriarDados(userModel: userModel):
        try:


            if not userModel.nome or userModel.nome.strip() == "":
                raise HTTPException(status_code=400, detail="O nome não pode ser vazio")
            if not userModel.sobrenome or userModel.sobrenome.strip() == "":
                raise HTTPException(status_code=400, detail="O sobrenome não pode ser vazio")
            if not userModel.email or userModel.email.strip() == "":
                raise HTTPException(status_code=400, detail="O email não pode ser vazio")
            if not userModel.telefone or userModel.telefone.strip() == "":
                raise HTTPException(status_code=400, detail="O telefone não pode ser vazio")
            
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

            
            if dados_atualizados.email and len(dados_atualizados.email) > 20:
                raise HTTPException(status_code=400, detail="O email não pode ter mais de 20 caracteres")
            
            
            if dados_atualizados.telefone and len(dados_atualizados.telefone) > 11:
                raise HTTPException(status_code=400, detail="O telefone não pode ter mais de 11 caracteres")


            if dados_atualizados.telefone and not re.fullmatch(r'\d+', dados_atualizados.telefone):
                raise HTTPException(status_code=400, detail="O número de telefone deve conter apenas números")

            if dados_atualizados.email and not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", dados_atualizados.email):
                raise HTTPException(status_code=422, detail="O email contém caracteres inválidos")

            email_duplicado = Usuario.find_one({"email": dados_atualizados.email, "id": {"$ne": user_id}})
            if email_duplicado:
                raise HTTPException(status_code=422, detail="Já existe um usuário com este email")

            telefone_duplicado = Usuario.find_one({"telefone": dados_atualizados.telefone, "id": {"$ne": user_id}})
            if telefone_duplicado:
                raise HTTPException(status_code=422, detail="Já existe um usuário com este telefone")


            update_data = {}

            if dados_atualizados.nome:
                update_data["nome"] = dados_atualizados.nome
            
            if dados_atualizados.sobrenome:
                update_data["sobrenome"] = dados_atualizados.sobrenome
            
            if dados_atualizados.email:
                update_data["email"] = dados_atualizados.email.lower()
            
            if dados_atualizados.telefone:
                update_data["telefone"] = dados_atualizados.telefone
            
            update_data["dataatualizacao"] = datetime.now()

            if update_data:
                resultado = Usuario.update_one(
                    {"id": user_id},
                    {"$set": update_data}
                )
                
                if resultado.matched_count == 0:
                    raise HTTPException(status_code=422, detail="Erro ao atualizar o usuário")

                return {"message": "Usuário atualizado com sucesso!"}
            else:
                raise HTTPException(status_code=400, detail="Nenhum campo foi fornecido para atualização")

        except Exception as error:
            raise HTTPException(status_code=400, detail=str(error))
