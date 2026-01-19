@echo off
title FANGIO TELECOM - Aplicacion Multi-Usuario
color 0A

echo ========================================
echo    FANGIO TELECOM - SISTEMA ROBUSTO
echo ========================================
echo.
echo Configurando aplicacion para multiples usuarios...
echo.

:: Verificar si estamos en el directorio correcto
if not exist "app.py" (
    echo ERROR: No se encontro app.py
    echo Asegurate de ejecutar este script desde el directorio nuevo_baseado
    pause
    exit /b 1
)

:: Instalar dependencias si es necesario
echo [1/4] Verificando dependencias...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

:: Limpiar procesos Excel existentes
echo [2/4] Limpiando procesos Excel existentes...
taskkill /f /im excel.exe >nul 2>&1
timeout /t 2 /nobreak >nul

:: Limpiar archivos temporales
echo [3/4] Limpiando archivos temporales...
if exist "site_survey\*.xlsx" (
    del /q "site_survey\*.xlsx" >nul 2>&1
)
if exist "ptmp_site_survey\*.xlsx" (
    del /q "ptmp_site_survey\*.xlsx" >nul 2>&1
)

:: Iniciar aplicación
echo [4/4] Iniciando aplicacion Flask...
echo.
echo ========================================
echo    APLICACION INICIADA EXITOSAMENTE
echo ========================================
echo.
echo URLs disponibles:
echo   - Local: http://127.0.0.1:5000
echo   - Red: http://192.168.1.18:5000
echo.
echo Caracteristicas activas:
echo   ✓ Soporte para 10 usuarios simultaneos
echo   ✓ Gestion automatica de procesos Excel
echo   ✓ Limpieza automatica de archivos temporales
echo   ✓ Timeout de sesion: 30 minutos
echo.
echo Para detener la aplicacion: Ctrl+C
echo ========================================
echo.

python app.py

echo.
echo Aplicacion detenida.
pause 