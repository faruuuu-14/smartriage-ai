@echo off
title SmarTriage-Wound AI Backend Server
echo ========================================================
echo    Menjalankan Backend SmarTriage-Wound AI (FastAPI)
echo ========================================================
cd backend
echo Mengakses Dokumentasi API di: http://localhost:8000/docs
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
