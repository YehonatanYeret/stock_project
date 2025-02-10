# Kill old server process if it's still running
$serverProcess = Get-Process | Where-Object { $_.ProcessName -match "Server" }
if ($serverProcess) {
    Stop-Process -Id $serverProcess.Id -Force
    Start-Sleep -Seconds 2
}

# Ensure server port is free
$port = 5039
$serverPortProcess = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($serverPortProcess) {
    Write-Host "⚠️ Port $port is in use! Killing the process..."
    Stop-Process -Id $serverPortProcess -Force
    Start-Sleep -Seconds 2
}

## Clean old build files
#Write-Host "Cleaning old build files..."
#dotnet clean "server"
#
## Build the server project before running
#Write-Host "Building server..."
#dotnet build "server"
#if ($LASTEXITCODE -ne 0) {
#    Write-Host "❌ Build failed! Exiting..."
#    exit 1
#}

# Start the server in the background
Write-Host "✅ Build succeeded! Starting server..."
$server = Start-Process -NoNewWindow -PassThru -FilePath "dotnet" -ArgumentList "run --project server"

# Ensure server is running before starting the client
Start-Sleep -Seconds 3
if ($server.HasExited) {
    Write-Host "❌ Server crashed after startup! Exiting..."
    exit 1
}

# Check if the virtual environment is active
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️ Virtual environment is not active."

    # Check if the virtual environment exists
    if (-Not (Test-Path "client\venv")) {
        Write-Host "🔧 Virtual environment not found. Creating one..."
        python -m venv client\venv
        Write-Host "✅ Virtual environment created successfully."
    }

    # Activate the virtual environment
    Write-Host "Activating virtual environment..."
    & "client\venv\Scripts\activate"

    # Install dependencies
    if (Test-Path "client\requirements.txt") {
        Write-Host "📦 Installing dependencies from requirements.txt..."
        pip install -r client\requirements.txt
        Write-Host "✅ Dependencies installed successfully."
    } else {
        Write-Host "⚠️ requirements.txt not found. Skipping dependency installation."
    }
} else {
    Write-Host "✅ Virtual environment is already active."
}


# Run the client
Write-Host "Starting client..."

Write-Host ""
Write-Host ""
Write-Host "!!!יהונתן הגבר!!!" -ForegroundColor Black -BackgroundColor Yellow
Write-Host "!!!הכי גבר שיש!!!" -ForegroundColor White -BackgroundColor Red
Write-Host ""
Write-Host ""
$clientProcess = Start-Process -NoNewWindow -PassThru -FilePath "python" -ArgumentList "client\main.py"

# Monitor the client process
$clientProcess.WaitForExit()
if ($clientProcess.ExitCode -ne 0) {
    Write-Host "❌ Client encountered an error! Exiting..."
    Stop-Process -Id $server.Id -Force
    exit 1
}

Write-Host "✅ Client exited successfully."
Write-Host "CRITICAL ERROR: Unable to continue!" -ForegroundColor Black -BackgroundColor Yellow
