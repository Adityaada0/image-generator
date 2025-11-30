@echo off
REM Setup script for Image Generator on Windows

echo.
echo ==========================================
echo  CPU/Integrated GPU Image Generator Setup
echo ==========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Installing Python packages...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo [2/3] Creating output directory...
if not exist "outputs" mkdir outputs

echo.
echo [3/3] Setup complete!
echo.
echo ==========================================
echo  Setup Finished Successfully!
echo ==========================================
echo.
echo To start the web interface, run:
echo   python app.py
echo.
echo Then open your browser to: http://localhost:5000
echo.
echo For command-line usage, run:
echo   python generate.py
echo.
pause
