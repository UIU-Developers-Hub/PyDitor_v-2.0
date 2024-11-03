# File: backend/run_coverage.bat
@echo off
REM Windows batch script to run coverage
pytest --cov=app --cov-report=term-missing --cov-report=html
if %ERRORLEVEL% == 0 (
    echo Opening coverage report...
    start coverage_html\index.html
)
