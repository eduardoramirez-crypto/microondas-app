@echo off
echo ========================================
echo    CONFIGURADOR GIT - FANGIO TELECOM
echo ========================================
echo.

echo [1/6] Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git no está instalado
    echo Por favor instala Git desde: https://git-scm.com/download/win
    echo O ejecuta: winget install Git.Git
    pause
    exit /b 1
) else (
    echo ✅ Git encontrado
    git --version
)

echo.
echo [2/6] Configurando Git...
set /p GIT_NAME="Ingresa tu nombre completo: "
set /p GIT_EMAIL="Ingresa tu email: "

git config --global user.name "%GIT_NAME%"
git config --global user.email "%GIT_EMAIL%"

echo ✅ Git configurado para: %GIT_NAME% <%GIT_EMAIL%>

echo.
echo [3/6] Inicializando repositorio...
if exist ".git" (
    echo ✅ Repositorio Git ya existe
) else (
    git init
    echo ✅ Repositorio Git inicializado
)

echo.
echo [4/6] Configurando repositorio remoto...
set /p GITHUB_URL="Ingresa la URL de tu repositorio GitHub (ej: https://github.com/usuario/fangio-telecom-project.git): "

git remote remove origin 2>nul
git remote add origin "%GITHUB_URL%"

echo ✅ Repositorio remoto configurado: %GITHUB_URL%

echo.
echo [5/6] Preparando primer commit...
git add .

echo.
echo [6/6] Haciendo commit inicial...
git commit -m "🎉 Commit inicial: Sistema Fangio Telecom completo

- Páginas principales: ptpFangio.html, ptmpFangio.html
- Aplicación Python Flask en nuevo_baseado/
- Scripts de instalación y configuración
- Documentación completa
- Sistema de backup automático
- Configuración GitHub Actions
- Templates de issues"

echo.
echo ========================================
echo    CONFIGURACIÓN COMPLETADA
echo ========================================
echo.
echo Para subir a GitHub, ejecuta:
echo git push -u origin main
echo.
echo Si tienes problemas con 'main' vs 'master':
echo git branch -M main
echo git push -u origin main
echo.
echo Presiona cualquier tecla para continuar...
pause >nul

echo.
echo ¿Quieres subir el código a GitHub ahora? (s/n): 
set /p SUBIR=""

if /i "%SUBIR%"=="s" (
    echo.
    echo Subiendo a GitHub...
    git branch -M main
    git push -u origin main
    
    if errorlevel 1 (
        echo ❌ Error al subir a GitHub
        echo Verifica tu URL y credenciales
    ) else (
        echo ✅ Código subido exitosamente a GitHub
    )
) else (
    echo.
    echo Recuerda ejecutar manualmente:
    echo git push -u origin main
)

echo.
echo ¡Configuración completada! 🚀
pause 