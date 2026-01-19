@echo off
echo ========================================
echo    DIAGNOSTICO DE LA APLICACION
echo ========================================
echo.

cd /d "%~dp0"
echo Directorio actual: %CD%
echo.

echo Ejecutando diagnostico...
python diagnostico.py

echo.
echo ========================================
echo Presiona cualquier tecla para continuar...
pause >nul
