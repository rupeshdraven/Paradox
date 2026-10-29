@echo off
setlocal
cd /d "%~dp0"
echo ========================================================
echo Pushing Paradox / FinWise AI to GitHub:
echo https://github.com/rupeshdraven/Paradox.git
echo ========================================================
echo.
git push -u origin main
echo.
if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] FinWise AI repository pushed to GitHub successfully!
) else (
    echo.
    echo [NOTICE] If prompted by Windows Git Credential Manager:
    echo 1. Click "Sign in with your browser"
    echo    OR
    echo 2. Enter your GitHub Personal Access Token (PAT).
)
pause

