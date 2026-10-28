@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
set PYTHONPATH=%~dp0
echo Starting AI Co-Pilot for SEBI-Registered Investment Advisers...
echo Note: Prototype designed around the Zeckathon PS4 requirements; not SEBI-approved or certified.
echo Opening in browser: http://127.0.0.1:8501
.\.venv\Scripts\streamlit.exe run app/main.py --server.address=127.0.0.1 --server.port=8501
pause
