from fastapi import APIRouter
from app.api.v1.endpoints import triage

api_router = APIRouter()
api_router.include_router(triage.router, prefix="/triage", tags=["Triase & Analisis Luka"])
