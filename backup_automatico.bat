@echo off
echo ========================================
echo    BACKUP AUTOMÁTICO - FANGIO TELECOM
echo ========================================
echo.

:: Configurar fecha y hora
set FECHA=%date:~-4,4%-%date:~-10,2%-%date:~-7,2%
set HORA=%time:~0,2%-%time:~3,2%-%time:~6,2%
set HORA=%HORA: =0%

:: Crear directorio de backup
set BACKUP_DIR=backup_%FECHA%_%HORA%
mkdir "%BACKUP_DIR%"

echo [1/4] Creando backup de datos...
echo Fecha: %FECHA% %HORA%

:: Copiar archivos importantes
echo [2/4] Copiando archivos...

:: Copiar carpeta de uploads
if exist "nuevo_baseado\uploads" (
    xcopy "nuevo_baseado\uploads" "%BACKUP_DIR%\uploads\" /E /I /Y
    echo ✅ Uploads copiados
)

:: Copiar archivos de configuración
if exist "config.js" (
    copy "config.js" "%BACKUP_DIR%\"
    echo ✅ Configuración copiada
)

:: Copiar archivos de datos
if exist "*.xlsx" (
    copy "*.xlsx" "%BACKUP_DIR%\"
    echo ✅ Archivos Excel copiados
)

if exist "*.csv" (
    copy "*.csv" "%BACKUP_DIR%\"
    echo ✅ Archivos CSV copiados
)

:: Crear archivo de información del backup
echo [3/4] Creando registro de backup...

echo Backup realizado el %FECHA% a las %HORA% > "%BACKUP_DIR%\info_backup.txt"
echo. >> "%BACKUP_DIR%\info_backup.txt"
echo Archivos incluidos: >> "%BACKUP_DIR%\info_backup.txt"
dir "%BACKUP_DIR%" /B >> "%BACKUP_DIR%\info_backup.txt"

:: Comprimir backup (si hay 7zip)
echo [4/4] Comprimiendo backup...
if exist "C:\Program Files\7-Zip\7z.exe" (
    "C:\Program Files\7-Zip\7z.exe" a "%BACKUP_DIR%.zip" "%BACKUP_DIR%\*" -r
    rmdir "%BACKUP_DIR%" /S /Q
    echo ✅ Backup comprimido: %BACKUP_DIR%.zip
) else (
    echo ⚠️ 7-Zip no encontrado, backup sin comprimir
    echo ✅ Backup creado en: %BACKUP_DIR%
)

:: Limpiar backups antiguos (mantener solo 7 días)
echo.
echo 🧹 Limpiando backups antiguos...
forfiles /p . /m backup_*.zip /d -7 /c "cmd /c del @path" 2>nul
forfiles /p . /m backup_* /d -7 /c "cmd /c rmdir @path /s /q" 2>nul

echo.
echo ========================================
echo    BACKUP COMPLETADO
echo ========================================
echo.
echo 📁 Ubicación: %BACKUP_DIR%.zip
echo 📅 Fecha: %FECHA% %HORA%
echo 📊 Tamaño: 
if exist "%BACKUP_DIR%.zip" (
    for %%A in ("%BACKUP_DIR%.zip") do echo    %%~zA bytes
)
echo.
echo ✅ Backup guardado exitosamente
echo.
pause 