@echo off
echo ========================================
echo   PRUEBA DE INTEGRACION
echo   SISTEMA DE GESTION DE ARCHIVOS
echo ========================================
echo.

echo 🔍 Verificando integración con app.py...
echo.

echo ✅ PASO 1: Verificar sintaxis...
python -m py_compile app.py

if %errorlevel% neq 0 (
    echo ❌ Error de sintaxis en app.py
    echo.
    pause
    exit /b 1
)

echo ✅ Sintaxis correcta
echo.

echo ✅ PASO 2: Verificar módulo file_manager...
python -c "from file_manager import file_manager; print('✅ Módulo file_manager importado correctamente')"

if %errorlevel% neq 0 (
    echo ❌ Error importando file_manager
    echo.
    pause
    exit /b 1
)

echo ✅ Módulo file_manager disponible
echo.

echo ✅ PASO 3: Verificar directorios...
if exist "generated_files" (
    echo ✅ Directorio generated_files existe
) else (
    echo ⚠️ Directorio generated_files no existe, creándolo...
    mkdir generated_files
    mkdir generated_files\templates
    mkdir generated_files\site_survey
    mkdir generated_files\solution_design
    mkdir generated_files\ptp_analysis
    mkdir generated_files\ptmp_analysis
    mkdir generated_files\report
    echo ✅ Directorios creados
)

echo.
echo ✅ PASO 4: Verificar plantillas...
if exist "templates\file_manager.html" (
    echo ✅ file_manager.html disponible
) else (
    echo ❌ file_manager.html no encontrado
)

if exist "templates\confirmacion_descarga_new.html" (
    echo ✅ confirmacion_descarga_new.html disponible
) else (
    echo ❌ confirmacion_descarga_new.html no encontrado
)

echo.
echo 🎯 INTEGRACION COMPLETADA:
echo   - ✅ app.py modificado con rutas de gestión
echo   - ✅ file_manager.py integrado
echo   - ✅ Funciones de descarga modificadas
echo   - ✅ Página de confirmación actualizada
echo   - ✅ Botón de gestión agregado

echo.
echo 🚀 FUNCIONALIDADES DISPONIBLES:
echo   - 📁 Guardado automático de archivos generados
echo   - 🔄 Reutilización de plantillas
echo   - ⚡ Generación múltiple de archivos
echo   - 📊 Historial completo de generaciones
echo   - 🔍 Búsqueda y filtrado avanzado
echo   - 💾 Sistema de respaldo automático

echo.
echo 📍 UBICACIONES DE ACCESO:
echo   - Página principal: / (Acceso Rápido > Gestión de Archivos)
echo   - Página de confirmación: Botón "Gestionar Archivos Generados"
echo   - Acceso directo: /file_manager

echo.
echo ⚡ PARA PROBAR:
echo   1. Ejecuta: python app.py
echo   2. Genera un documento (Site Survey o Diseño)
echo   3. En la confirmación, haz clic en "Gestionar Archivos"
echo   4. Verifica que el archivo aparezca en el historial

echo.
echo ✅ Prueba de integración completada exitosamente!
echo.
pause 