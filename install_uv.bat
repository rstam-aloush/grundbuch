@echo off

chcp 65001 >nul

echo ==============================
echo [1] Installiere uv über winget...
echo ==============================
winget install --id=astral-sh.uv  -e

pause