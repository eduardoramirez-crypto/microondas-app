@echo off
chcp 65001 >nul
title Servidor Local para ptpFangio.html

echo.
echo ========================================
echo    🚀 SERVIDOR LOCAL PARA PTPFANGIO
echo ========================================
echo.

echo 📁 Verificando archivos...
if not exist "ptpFangio.html" (
    echo ❌ Error: No se encontró ptpFangio.html
    echo 💡 Asegúrate de ejecutar este archivo desde la carpeta correcta
    pause
    exit /b 1
)

echo ✅ Archivo ptpFangio.html encontrado

echo.
echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo 💡 Instala Python desde: https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado

echo.
echo 🚀 Iniciando servidor local...
echo 📋 URL: http://localhost:8000/ptpFangio.html
echo 💡 Para detener el servidor, presiona Ctrl+C
echo.

python iniciar_servidor.py

echo.
echo 🛑 Servidor detenido
pause 