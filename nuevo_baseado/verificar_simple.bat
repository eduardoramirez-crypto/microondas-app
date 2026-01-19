@echo off
echo ========================================
echo   VERIFICADOR SIMPLE DE APP.PY
echo ========================================
echo.

echo 🔍 PASO 1: Verificando sintaxis basica...
python -m py_compile app.py

if %errorlevel% equ 0 (
    echo ✅ Sintaxis correcta - No hay errores
    echo.
    echo 🔍 PASO 2: Verificando que Flask este disponible...
    python -c "from flask import Flask; print('✅ Flask disponible')"
    
    if %errorlevel% equ 0 (
        echo.
        echo 🎯 VERIFICACION COMPLETADA:
        echo   - Sintaxis: ✅ Correcta
        echo   - Flask: ✅ Disponible
        echo.
        echo 🚀 La aplicacion esta lista para ejecutar:
        echo   python app.py
    ) else (
        echo ❌ Flask no disponible
        echo.
        echo 💡 Instala Flask con:
        echo   pip install Flask
    )
) else (
    echo ❌ Error de sintaxis encontrado
    echo.
    echo 🔧 Revisa los errores arriba y corrijelos
    echo.
    echo 💡 Tipos de errores comunes:
    echo   - Variables globales mal declaradas
    echo   - Parentesis o llaves no balanceados
    echo   - Comas faltantes o extra
    echo   - Imports incorrectos
)

echo.
pause 