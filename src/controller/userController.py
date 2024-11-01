from fastapi import APIRouter, HTTPException
from src.models.userModel import userModel
from src.services.userService import userService
from src.models.respostasModel import Resposta
from typing import Optional, List

app_router = APIRouter(prefix="/hub")


@app_router.post('/criar', status_code=200, tags=["Usuários"])
async def CriarDados(userModel: userModel):
   return await userService.CriarDados(userModel)

@app_router.delete("/remover", status_code=200, tags=["Usuários"])
async def RemoverUsuario(user_id: int):
    return await userService.RemoverUsuario(user_id)

@app_router.get("/listarUsers", status_code=200, tags=["Usuários"])
async def BuscarUsuario(
    user_id: Optional[int] = None, 
    nome: Optional[str] = None, 
    email: Optional[str] = None, 
    telefone: Optional[str] = None
):
    return await userService.BuscarUsuario(user_id=user_id, nome=nome, email=email, telefone=telefone)



@app_router.post("/AtualizarUm", status_code=200, tags=["Usuários"])
async def AtualizarCliente(user_id: int, dados_atualizados: userModel):
    return await userService.AtualizarCliente(user_id, dados_atualizados)
