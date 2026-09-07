"""
Aplikasi Utama FastAPI - SmarTriage-Wound AI Backend & Web UI
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Backend API Cerdas untuk Triase Pertolongan Pertama dan Analisis Luka Berbasis Explainable AI (Grad-CAM)"
)

# Konfigurasi CORS agar bisa diakses oleh aplikasi Android (Emulator/Real Device) dan Web Browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount folder static untuk menyajikan file gambar heatmap Grad-CAM dan aset statis
if os.path.exists(settings.STATIC_DIR):
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# Sertakan router API v1
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Antarmuka Web"])
def serve_web_ui():
    """Menampilkan antarmuka web interaktif yang modern, bersih, dan rapi"""
    index_path = os.path.join(settings.STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "status": "online",
        "system": settings.PROJECT_NAME,
        "docs_url": "/docs"
    }

@app.get("/health", tags=["Health Check"])
def health_check():
    return {
        "status": "online",
        "system": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION
    }
