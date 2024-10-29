:: scripts/activate.bat
@echo off
echo Activating PyDitor virtual environment...

:: Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run initialization script first.
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Verify activation
python -V
where python

echo.
echo Virtual environment activated successfully!
echo Type 'deactivate' to exit the virtual environment