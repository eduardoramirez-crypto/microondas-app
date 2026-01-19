@echo off
echo ========================================
echo    CREADOR DE PAQUETE FANGIO TELECOM
echo ========================================
echo.

echo [1/3] Creando carpeta temporal...
set FECHA=%date:~-4,4%-%date:~-10,2%-%date:~-7,2%
set HORA=%time:~0,2%-%time:~3,2%-%time:~6,2%
set HORA=%HORA: =0%

set PAQUETE_DIR=Fangio_Telecom_%FECHA%_%HORA%
mkdir "%PAQUETE_DIR%"

echo ✅ Carpeta creada: %PAQUETE_DIR%

echo.
echo [2/3] Copiando archivos...
xcopy "*.html" "%PAQUETE_DIR%\" /Y /Q
xcopy "*.bat" "%PAQUETE_DIR%\" /Y /Q
xcopy "*.py" "%PAQUETE_DIR%\" /Y /Q
xcopy "*.md" "%PAQUETE_DIR%\" /Y /Q
xcopy "*.txt" "%PAQUETE_DIR%\" /Y /Q
xcopy "*.js" "%PAQUETE_DIR%\" /Y /Q
xcopy "nuevo_baseado" "%PAQUETE_DIR%\nuevo_baseado\" /E /I /Y /Q
xcopy "img" "%PAQUETE_DIR%\img\" /E /I /Y /Q

echo ✅ Archivos copiados

echo.
echo [3/3] Creando archivo ZIP...
if exist "C:\Program Files\7-Zip\7z.exe" (
    "C:\Program Files\7-Zip\7z.exe" a "%PAQUETE_DIR%.zip" "%PAQUETE_DIR%\*" -r
    rmdir "%PAQUETE_DIR%" /S /Q
    echo ✅ Paquete creado: %PAQUETE_DIR%.zip
) else (
    echo ⚠️ 7-Zip no encontrado
    echo ✅ Paquete creado en carpeta: %PAQUETE_DIR%
    echo Para crear ZIP manualmente:
    echo 1. Click derecho en la carpeta
    echo 2. "Enviar a" > "Carpeta comprimida"
)

echo.
echo ========================================
echo    PAQUETE LISTO PARA ENVIAR
echo ========================================
echo.
echo 📁 Ubicación: %PAQUETE_DIR%.zip
echo 📅 Fecha: %FECHA% %HORA%
echo.
echo 📤 Para enviar:
echo 1. WhatsApp: Adjuntar archivo
echo 2. Telegram: Adjuntar archivo
echo 3. Email: Adjuntar archivo
echo 4. Google Drive: Subir archivo
echo.
echo 📋 Instrucciones para el equipo:
echo 1. Descargar y extraer ZIP
echo 2. Ejecutar: instalar_proyecto.bat
echo 3. Acceder: http://127.0.0.1:5000
echo.
pause 