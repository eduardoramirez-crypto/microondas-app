@echo off
echo ========================================
echo    CONECTANDO A TU SERVIDOR DIGITALOCEAN
echo ========================================
echo.
echo IP del servidor: 137.184.246.51
echo Usuario: root
echo.
echo ========================================
echo.

REM Verificar si SSH está disponible
where ssh >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: SSH no está instalado en tu sistema.
    echo.
    echo SOLUCIONES:
    echo 1. Instalar Git Bash (incluye SSH)
    echo 2. Usar PuTTY (gratuito)
    echo 3. Usar Windows Terminal
    echo.
    pause
    exit /b 1
)

echo Conectando al servidor...
echo.
echo Cuando te pida la contraseña, usa la que creaste en DigitalOcean.
echo.
ssh root@137.184.246.51

echo.
echo ========================================
echo    CONEXION TERMINADA
echo ========================================
pause 