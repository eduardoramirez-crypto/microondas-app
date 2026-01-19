@echo off
title FANGIO TELECOM - Aplicacion + Ngrok
color 0B

echo ========================================
echo    FANGIO TELECOM - ACCESO REMOTO
echo ========================================
echo.
echo Iniciando aplicacion con acceso remoto...
echo.

:: Verificar si estamos en el directorio correcto
if not exist "app.py" (
    echo ERROR: No se encontro app.py
    echo Asegurate de ejecutar este script desde el directorio nuevo_baseado
    pause
    exit /b 1
)

if not exist "ngrok.exe" (
    echo ERROR: No se encontro ngrok.exe
    echo Descarga ngrok desde https://ngrok.com/download
    pause
    exit /b 1
)

:: Instalar dependencias
echo [1/5] Verificando dependencias...
pip install -r requirements.txt --quiet

:: Limpiar procesos existentes
echo [2/5] Limpiando procesos existentes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im ngrok.exe >nul 2>&1
taskkill /f /im excel.exe >nul 2>&1
timeout /t 3 /nobreak >nul

:: Limpiar archivos temporales
echo [3/5] Limpiando archivos temporales...
if exist "site_survey\*.xlsx" del /q "site_survey\*.xlsx" >nul 2>&1
if exist "ptmp_site_survey\*.xlsx" del /q "ptmp_site_site_survey\*.xlsx" >nul 2>&1

:: Iniciar aplicación Flask en segundo plano
echo [4/5] Iniciando aplicacion Flask...
start "Flask App" cmd /c "python app.py"

:: Esperar a que Flask inicie
echo Esperando a que Flask inicie...
timeout /t 5 /nobreak >nul

:: Verificar que Flask esté corriendo
echo [5/5] Verificando que Flask esté corriendo...
timeout /t 3 /nobreak >nul

:: Iniciar ngrok
echo.
echo ========================================
echo    INICIANDO TUNEL NGROK
echo ========================================
echo.
echo La aplicacion Flask ya está corriendo.
echo Ahora se iniciará ngrok para acceso remoto.
echo.
echo URLs disponibles:
echo   - Local: http://127.0.0.1:5000
echo   - Remoto: https://[URL-NGROK].ngrok-free.app
echo.
echo Para detener: Cierra esta ventana
echo ========================================
echo.

:: Iniciar ngrok
ngrok.exe http 5000

echo.
echo Ngrok detenido.
pause 