@echo off

echo ==============================
echo  Installiere Python-Pakete...
echo ==============================
uv sync --frozen

echo ==============================
echo Starte das Python-Programm...
echo ==============================
uv run gb_historie.py

pause