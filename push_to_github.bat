@echo off
setlocal
cd /d "%~dp0"
echo ========================================================
echo Pushing PS4 AI-Powered Advisory to GitHub:
echo https://github.com/rupeshdraven/AIPowered-Advisory.git
echo ========================================================
echo.
git push -u origin main
echo.
if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Repository pushed to GitHub successfully!
) else (
    echo [NOTICE] If prompted, complete the sign-in in your browser or paste a GitHub Personal Access Token.
)
pause
