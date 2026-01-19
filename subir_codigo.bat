@echo off
echo ========================================
echo    SUBIENDO CODIGO AL SERVIDOR
echo ========================================
echo.
echo IP del servidor: 137.184.246.51
echo Directorio destino: /var/www/fangio-app
echo.
echo ========================================
echo.

REM Crear archivo ZIP con el proyecto
echo Creando archivo ZIP del proyecto...
powershell -command "Compress-Archive -Path 'nuevo_baseado\*' -DestinationPath 'fangio-app.zip' -Force"

if %errorlevel% neq 0 (
    echo ERROR: No se pudo crear el archivo ZIP.
    pause
    exit /b 1
)

echo Archivo ZIP creado exitosamente.
echo.

REM Subir archivo ZIP al servidor
echo Subiendo archivo al servidor...
echo Cuando te pida la contraseña, usa la que creaste en DigitalOcean.
echo.
scp fangio-app.zip root@137.184.246.51:/var/www/fangio-app/

if %errorlevel% neq 0 (
    echo ERROR: No se pudo subir el archivo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    ARCHIVO SUBIDO EXITOSAMENTE
echo ========================================
echo.
echo Ahora conectate al servidor y ejecuta:
echo cd /var/www/fangio-app
echo unzip fangio-app.zip
echo.
pause 