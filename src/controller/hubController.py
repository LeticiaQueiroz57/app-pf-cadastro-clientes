from fastapi import APIRouter, HTTPException
from src.models.hubModel import HubModel

hub_retour = APIRouter (prefix="api/hub")




@hub_retour.get("/list")
def listar_usuarios():
    return 0

