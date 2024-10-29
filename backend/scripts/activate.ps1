# scripts/activate.ps1
$ErrorActionPreference = "Stop"

# Get script location and project root
$scriptPath = $PSScriptRoot
$projectRoot = Split-Path -Parent $scriptPath
$venvPath = Join-Path -Path $projectRoot -ChildPath "venv"

Write-Output "Activating PyDitor virtual environment..."

try {
    # Check if virtual environment exists
    if (-not (Test-Path -Path "$venvPath\Scripts\Activate.ps1")) {
        Write-Output "Virtual environment not found. Please run initialization script first."
        exit 1
    }

    # Activate virtual environment
    & "$venvPath\Scripts\Activate.ps1"

    # Verify activation
    if ($env:VIRTUAL_ENV) {
        Write-Output "Virtual environment activated successfully!"
        Write-Output "Python path: $(Get-Command python | Select-Object -ExpandProperty Source)"
        Write-Output "Python version: $(python -V)"
    } else {
        Write-Output "Failed to activate virtual environment."
        exit 1
    }
} catch {
    Write-Output "Error activating virtual environment: $_"
    exit 1
}