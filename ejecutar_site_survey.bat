@echo off
title Site Survey App - Fangio Telecom
color 0B

echo.
echo ========================================
echo    SITE SURVEY APP - FANGIO TELECOM
echo ========================================
echo.
echo Iniciando aplicacion Python...
echo.

cd /d "%~dp0nuevo_baseado"

echo Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

echo.
echo Instalando dependencias...
pip install -r requirements.txt 2>nul
if %errorlevel% neq 0 (
    echo Advertencia: No se pudo instalar requirements.txt
    echo Continuando sin dependencias adicionales...
)

echo.
echo Ejecutando aplicacion...
echo La aplicacion se abrira en: http://127.0.0.1:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python run_app.py

echo.
echo Aplicacion cerrada.
pause 