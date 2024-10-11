from fastapi import FastAPI, APIRouter
from src.controller.hubController import hub_retour



router = APIRouter()

app = FastAPI()

app.include_router(hub_retour)
