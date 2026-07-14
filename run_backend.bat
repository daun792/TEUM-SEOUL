@echo off
setlocal
cd /d "%~dp0backend"

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python was not found. Install Python 3.11 or later.
  pause
  exit /b 1
)

python -c "import fastapi, uvicorn, sqlalchemy, dotenv" >nul 2>nul
if errorlevel 1 (
  echo Installing backend dependencies...
  python -m pip install -r requirements.txt
  if errorlevel 1 (
    echo [ERROR] Backend dependency installation failed.
    pause
    exit /b 1
  )
)

python scripts\init_db.py
if errorlevel 1 (
  echo [ERROR] Database initialization failed.
  pause
  exit /b 1
)

echo TeumSeoul API: http://localhost:8000
echo API docs: http://localhost:8000/docs
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
endlocal
