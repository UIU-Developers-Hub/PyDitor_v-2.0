# scripts/reset_venv.ps1
# Function to safely remove directory
function Remove-DirectorySafely {
    param (
        [string]$Path
    )
    
    if (Test-Path $Path) {
        Write-Host "Removing $Path..."
        try {
            # Kill any Python processes
            Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 2
            
            # Remove directory
            Remove-Item -Path $Path -Recurse -Force -ErrorAction Stop
            Write-Host "Successfully removed $Path"
        }
        catch {
            Write-Host "Failed to remove directory, trying alternative method..."
            # Alternative removal method using cmd
            cmd /c "rmdir /s /q $Path"
        }
    }
}

# Main script
Write-Host "Starting virtual environment reset..."

# Deactivate virtual environment if active
if (Test-Path "venv/Scripts/activate") {
    Write-Host "Deactivating virtual environment..."
    deactivate
}

# Remove existing venv
Remove-DirectorySafely "venv"

# Create new virtual environment
Write-Host "Creating new virtual environment..."
python -m venv venv

# Activate new environment
Write-Host "Activating new virtual environment..."
./venv/Scripts/Activate

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Virtual environment reset completed!"