# TermiBase Windows Installation Helper
# This script helps set up TermiBase on Windows by adding it to PATH

Write-Host "🚀 TermiBase Windows Setup" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Install TermiBase
Write-Host "📦 Installing TermiBase..." -ForegroundColor Cyan
python -m pip install --upgrade termibase

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Installation failed" -ForegroundColor Red
    exit 1
}

Write-Host "✓ TermiBase installed successfully!" -ForegroundColor Green
Write-Host ""

# Find Python Scripts directory
$pythonPath = python -c "import site; import os; print(os.path.join(os.path.dirname(site.getusersitepackages()), 'Scripts'))" 2>&1

if (-not $pythonPath) {
    # Fallback: try common locations
    $userProfile = $env:USERPROFILE
    $possiblePaths = @(
        "$userProfile\AppData\Roaming\Python\Python310\Scripts",
        "$userProfile\AppData\Roaming\Python\Python311\Scripts",
        "$userProfile\AppData\Roaming\Python\Python312\Scripts",
        "$userProfile\AppData\Local\Programs\Python\Python310\Scripts",
        "$userProfile\AppData\Local\Programs\Python\Python311\Scripts",
        "$userProfile\AppData\Local\Programs\Python\Python312\Scripts"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path "$path\termibase.exe") {
            $pythonPath = $path
            break
        }
    }
}

if (-not $pythonPath -or -not (Test-Path "$pythonPath\termibase.exe")) {
    Write-Host "⚠️  Could not find termibase.exe location" -ForegroundColor Yellow
    Write-Host "You can still use: python -m termibase" -ForegroundColor Cyan
    exit 0
}

Write-Host "Found TermiBase at: $pythonPath" -ForegroundColor Cyan
Write-Host ""

# Check if already in PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -like "*$pythonPath*") {
    Write-Host "✓ Scripts directory is already in PATH!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 You can now use:" -ForegroundColor Green
    Write-Host "   termibase" -ForegroundColor Cyan
    exit 0
}

# Ask user if they want to add to PATH
Write-Host "Would you like to add this directory to your PATH?" -ForegroundColor Yellow
Write-Host "This will allow you to use 'termibase' command directly." -ForegroundColor Yellow
Write-Host ""
$response = Read-Host "Add to PATH? (Y/n)"

if ($response -eq "n" -or $response -eq "N") {
    Write-Host ""
    Write-Host "✓ Installation complete!" -ForegroundColor Green
    Write-Host "You can use: python -m termibase" -ForegroundColor Cyan
    exit 0
}

# Add to PATH
try {
    $newPath = $currentPath + ";$pythonPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host ""
    Write-Host "✓ Added to PATH successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  Please restart your terminal for changes to take effect." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🎉 After restarting, you can use:" -ForegroundColor Green
    Write-Host "   termibase" -ForegroundColor Cyan
} catch {
    Write-Host ""
    Write-Host "❌ Failed to add to PATH automatically" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please add this directory to PATH manually:" -ForegroundColor Yellow
    Write-Host "   $pythonPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or use: python -m termibase" -ForegroundColor Cyan
}

