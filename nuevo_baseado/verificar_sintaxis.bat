@echo off
echo ========================================
echo   VERIFICADOR DE SINTAXIS PYTHON
echo ========================================
echo.

echo 🔍 Verificando sintaxis de app.py...
python -m py_compile app.py

if %errorlevel% equ 0 (
    echo ✅ Sintaxis correcta - No hay errores
    echo.
    echo 🚀 Puedes ejecutar la aplicación:
    echo   python app.py
) else (
    echo ❌ Error de sintaxis encontrado
    echo.
    echo 🔧 Revisa los errores arriba y corrígelos
    echo.
    echo 💡 Tipos de errores comunes:
    echo   - Variables globales mal declaradas
    echo   - Paréntesis o llaves no balanceados
    echo   - Comas faltantes o extra
    echo   - Imports incorrectos
)

echo.
pause 