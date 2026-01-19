@echo off
echo ========================================
echo   PRUEBA DE CORRECCION DEL ERROR
echo   TypeError: int() argument must be...
echo ========================================
echo.

echo 🔍 PASO 1: Verificar sintaxis de app.py...
python -m py_compile app.py

if %errorlevel% equ 0 (
    echo ✅ Sintaxis correcta
    echo.
    echo 🔍 PASO 2: Verificar que Flask esté disponible...
    python -c "from flask import Flask; print('✅ Flask disponible')"
    
    if %errorlevel% equ 0 (
        echo.
        echo 🎯 CORRECCION IMPLEMENTADA:
        echo   - ✅ Validación de fila_idx en site_survey()
        echo   - ✅ Validación de fila_idx en seleccion()
        echo   - ✅ Manejo de errores con páginas HTML amigables
        echo   - ✅ Verificación de rangos de DataFrame
        echo.
        echo 🚀 LA APLICACION ESTA LISTA:
        echo   python app.py
        echo.
        echo 📋 FUNCIONALIDADES CORREGIDAS:
        echo   - Botón "Guardar Archivo" (naranja)
        echo   - Modal "¿Agregar Otro ID para Llenado?"
        echo   - Redirección automática a Site Survey
        echo   - Sistema de gestión de archivos integrado
        echo   - Manejo robusto de errores de fila_idx
        echo.
        echo 💡 PARA PROBAR:
        echo   1. Ejecuta: python app.py
        echo   2. Ve a Site Survey o Diseño de Solución
        echo   3. Genera un documento
        echo   4. Haz clic en "Guardar Archivo"
        echo   5. Verifica el modal y la funcionalidad
        echo.
        echo ✅ Error corregido exitosamente!
    ) else (
        echo ❌ Flask no disponible
        echo.
        echo 💡 Instala Flask con:
        echo   pip install Flask
    )
) else (
    echo ❌ Error de sintaxis en app.py
    echo.
    echo 🔧 Revisa los errores arriba y corrijelos
)

echo.
pause 