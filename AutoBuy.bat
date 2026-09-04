@echo off
title E7 AutoBuy
cd /d "%~dp0"

set "PY=C:\Users\mathe\AppData\Local\Python\pythoncore-3.14-64\python.exe"
if not exist "%PY%" set "PY=python"

"%PY%" autobuy_fixed.py

if errorlevel 1 (
    echo.
    echo Algo deu errado. Verifique o arquivo crash.log
    pause
)
