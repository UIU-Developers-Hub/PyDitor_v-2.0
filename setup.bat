@echo off
echo Setting up PyDitor v2 development environment...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH. Please install Python and try again.
    pause
    exit /b
)

:: Create virtual environment in 'venv' folder
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install project requirements
echo Installing project requirements...
pip install fastapi[all]
pip install uvicorn[standard]
pip install sqlalchemy[asyncio]
pip install alembic
pip install asyncpg
pip install psycopg2-binary
pip install python-dotenv

echo.
echo Setup complete! To activate the virtual environment manually:
echo ---------------------------------------------
echo In PowerShell: ^& .\venv\Scripts\Activate.ps1
echo In CMD: .\venv\Scripts\activate.bat
echo ---------------------------------------------

pause
