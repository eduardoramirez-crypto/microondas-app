@echo off
chcp 65001 >nul
title FANGIO TELECOM - Iniciar Aplicación

echo.
echo ========================================
echo    🚀 FANGIO TELECOM - SISTEMA WEB
echo ========================================
echo.

:: Verificar que existe el directorio nuevo_baseado
if not exist "nuevo_baseado" (
    echo ❌ ERROR: No se encontró el directorio 'nuevo_baseado'
    echo.
    echo Ubicación actual: %CD%
    echo.
    pause
    exit /b 1
)

:: Verificar que existe app.py
if not exist "nuevo_baseado\app.py" (
    echo ❌ ERROR: No se encontró el archivo 'app.py'
    echo.
    pause
    exit /b 1
)

:: Cambiar al directorio correcto
cd nuevo_baseado
echo ✅ Cambiado al directorio: %CD%
echo.

echo 🚀 Iniciando aplicación FANGIO TELECOM...
echo 📍 URL: http://127.0.0.1:5000
echo.

:: Esperar 2 segundos
timeout /t 2 /nobreak >nul

:: Abrir navegador
start http://127.0.0.1:5000
echo 🌐 Navegador abierto automáticamente
echo.

echo ========================================
echo 🎯 APLICACIÓN INICIADA CORRECTAMENTE
echo ========================================
echo 📋 Para detener: Ctrl+C
echo 🔄 Para reiniciar: Ejecuta este archivo nuevamente
echo ========================================
echo.

:: Ejecutar la aplicación Python
python app.py

:: Si llegamos aquí, la aplicación se cerró
echo.
echo 🛑 Aplicación cerrada
pause 