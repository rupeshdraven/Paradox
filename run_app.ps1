# PowerShell launcher for AI Co-Pilot for SEBI-Registered Investment Advisers
$env:PYTHONUTF8 = "1"
$env:PYTHONPATH = "$PSScriptRoot"
Set-Location -Path "$PSScriptRoot"
Write-Host "Starting AI Co-Pilot for SEBI-Registered Investment Advisers..." -ForegroundColor Cyan
Write-Host "Note: Prototype designed around the Zeckathon PS4 requirements; not SEBI-approved or certified." -ForegroundColor Yellow
Write-Host "Opening in browser: http://127.0.0.1:8501" -ForegroundColor Green
& ".\.venv\Scripts\streamlit.exe" run app/main.py --server.address=127.0.0.1 --server.port=8501
