# cleanup.ps1
Write-Host "Cleaning up project files..." -ForegroundColor Yellow

# Remove node_modules if it exists
if (Test-Path "node_modules") {
    Write-Host "Removing node_modules..." -ForegroundColor Cyan
    Remove-Item -Path "node_modules" -Recurse -Force -ErrorAction SilentlyContinue
}

# Remove package-lock.json if it exists
if (Test-Path "package-lock.json") {
    Write-Host "Removing package-lock.json..." -ForegroundColor Cyan
    Remove-Item -Path "package-lock.json" -Force -ErrorAction SilentlyContinue
}

# Remove TypeScript build info if it exists
if (Test-Path ".tsbuildinfo") {
    Write-Host "Removing .tsbuildinfo..." -ForegroundColor Cyan
    Remove-Item -Path ".tsbuildinfo" -Force -ErrorAction SilentlyContinue
}

Write-Host "Cleanup completed!" -ForegroundColor Green