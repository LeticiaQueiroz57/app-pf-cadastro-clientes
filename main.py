from fastapi import FastAPI, APIRouter
from src.controller.hubController import app_router

router = APIRouter()
app = FastAPI()

app.include_router(app_router)