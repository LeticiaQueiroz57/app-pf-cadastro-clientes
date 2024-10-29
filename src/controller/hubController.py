from fastapi import APIRouter, HTTPException
from src.models.hubModel import HubModel
from src.services.hubService import HubService
from src.models.respostasModel import Resposta


app_router = APIRouter(prefix="/hub")

@app_router.get("/list", status_code=200, tags=["Usuários"])
async def ListarTodos():
    resposta = await HubService.ListarTodos()
    return Resposta(resposta)

@app_router.post('/criar', status_code=200, tags=["Usuários"])
async def CriarDados(hubModel: HubModel):
    await HubService.CriarDados(hubModel)

@app_router.delete("/remover", status_code=200, tags=["Usuários"])
async def RemoverUsuario(user_id: int):
    return await HubService.RemoverUsuario(user_id)

@app_router.get("/pegar_um", status_code=200, tags= ["Usuários"])
async def BuscarUsuario(user_id: int):
    return await HubService.BuscarUsuario(user_id)
