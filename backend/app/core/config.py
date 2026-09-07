import os
from typing import List

class Settings:
    PROJECT_NAME: str = "SmarTriage-Wound AI"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Path konfigurasi direktori
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    STATIC_DIR: str = os.path.join(BASE_DIR, "static")
    HEATMAP_DIR: str = os.path.join(STATIC_DIR, "heatmaps")
    MODELS_DIR: str = os.path.join(BASE_DIR, "models")
    
    # CORS Origins (mengizinkan akses dari Android emulator, web browser, dll.)
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

settings = Settings()

# Pastikan folder static dan heatmaps tersedia
os.makedirs(settings.HEATMAP_DIR, exist_ok=True)
os.makedirs(settings.MODELS_DIR, exist_ok=True)
