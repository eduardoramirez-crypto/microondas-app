@echo off
echo ========================================
echo    FANGIO TELECOM - APLICACION WEB
echo ========================================
echo.

echo [1/3] Verificando directorio...
cd /d "%~dp0"
echo Directorio actual: %CD%
echo.

echo [2/3] Iniciando aplicacion Flask...
echo.
echo 🚀 La aplicacion se esta iniciando...
echo 📱 URL local: http://127.0.0.1:5000
echo 🌐 URL red: http://192.168.1.22:5000
echo.
echo ⚠️  NO CIERRES ESTA VENTANA
echo ⚠️  Mantenla abierta mientras uses la aplicacion
echo.

python app_simple_working.py

echo.
echo Aplicacion detenida.
pause 