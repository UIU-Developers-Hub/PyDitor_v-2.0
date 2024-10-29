# scripts/install_deps.ps1
# Function to install package
function Install-Package {
    param (
        [string]$Package,
        [string]$Version
    )
    
    Write-Host "Installing $Package==$Version..."
    python -m pip install --no-cache-dir "$Package==$Version"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install $Package" -ForegroundColor Red
        exit 1
    }
}

# Main script
Write-Host "Installing dependencies..."

# Core dependencies
$dependencies = @(
    @{Package="python-dotenv"; Version="1.0.0"},
    @{Package="psycopg2-binary"; Version="2.9.9"},
    @{Package="asyncpg"; Version="0.28.0"},
    @{Package="sqlalchemy"; Version="2.0.25"},
    @{Package="fastapi"; Version="0.109.0"},
    @{Package="uvicorn[standard]"; Version="0.27.0"},
    @{Package="alembic"; Version="1.13.1"},
    @{Package="pydantic"; Version="2.5.3"},
    @{Package="websockets"; Version="12.0"},
    @{Package="python-multipart"; Version="0.0.6"}
)

foreach ($dep in $dependencies) {
    Install-Package -Package $dep.Package -Version $dep.Version
}

Write-Host "All dependencies installed successfully!" -ForegroundColor Green