@echo off
echo ================================================
echo TB Prediction System - Startup Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/4] Python found!
echo [2/4] Node.js found!
echo.

REM Install Python dependencies if needed
if not exist "Lib\site-packages\fastapi" (
    echo [3/4] Installing Python dependencies...
    pip install -r requirements.txt
) else (
    echo [3/4] Python dependencies already installed
)

REM Install Node.js dependencies if needed
if not exist "node_modules" (
    echo [4/4] Installing Node.js dependencies...
    call npm install
) else (
    echo [4/4] Node.js dependencies already installed
)

echo.
echo ================================================
echo Starting servers...
echo ================================================
echo.
echo Backend API will start on: http://localhost:8000
echo Frontend UI will start on: http://localhost:5173
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop all servers
echo.

REM Start backend in background
start "TB Prediction Backend" cmd /k "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to initialize
timeout /t 5 /nobreak >nul

REM Start frontend
start "TB Prediction Frontend" cmd /k "npm run dev"

echo.
echo ================================================
echo Servers starting...
echo ================================================
echo.
echo If browsers don't open automatically, visit:
echo   - Frontend: http://localhost:5173
echo   - Backend: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo.
pause
