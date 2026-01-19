#!/usr/bin/env python3
"""
Script simple para crear el paquete de distribución
"""

import os
import shutil
import zipfile
from datetime import datetime

def main():
    print("📦 Creando paquete de distribución...")
    
    # Verificar que el ejecutable existe
    if not os.path.exists('dist/SiteSurveyApp.exe'):
        print("❌ No se encontró SiteSurveyApp.exe")
        return
    
    # Crear carpeta de distribución
    dist_folder = "SiteSurveyApp_Distribucion"
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    
    os.makedirs(dist_folder)
    print(f"📁 Carpeta creada: {dist_folder}")
    
    # Copiar ejecutable
    shutil.copy2('dist/SiteSurveyApp.exe', os.path.join(dist_folder, 'SiteSurveyApp.exe'))
    print("✅ SiteSurveyApp.exe copiado")
    
    # Crear script de instalación
    installer = '''@echo off
echo ========================================
echo    INSTALADOR SITE SURVEY APP
echo ========================================
echo.
echo Instalando Site Survey App...
set "DESKTOP=%USERPROFILE%\\Desktop"
set "APP_FOLDER=%DESKTOP%\\SiteSurveyApp"

echo Creando carpeta de aplicacion...
if not exist "%APP_FOLDER%" mkdir "%APP_FOLDER%"

echo Copiando archivos...
copy "SiteSurveyApp.exe" "%APP_FOLDER%\\"

echo Creando acceso directo...
echo @echo off > "%DESKTOP%\\Site Survey App.bat"
echo cd /d "%APP_FOLDER%" >> "%DESKTOP%\\Site Survey App.bat"
echo start "" "SiteSurveyApp.exe" >> "%DESKTOP%\\Site Survey App.bat"

echo.
echo ========================================
echo    INSTALACION COMPLETADA
echo ========================================
echo.
echo La aplicacion se ha instalado en:
echo %APP_FOLDER%
echo.
echo Puedes ejecutarla desde el acceso directo
echo en tu escritorio: "Site Survey App.bat"
echo.
echo IMPORTANTE:
echo - Si la app no se abre, ejecuta como administrador
echo - Verifica que Windows Defender no la bloquee
echo - La app usa puerto 5000 (cerrar otras apps si hay conflicto)
echo.
pause
'''
    
    with open(os.path.join(dist_folder, 'instalar.bat'), 'w') as f:
        f.write(installer)
    print("✅ instalar.bat creado")
    
    # Crear README
    readme = f'''# 🚀 Site Survey App - Instalación

## Instalación Rápida

1. **Ejecutar instalador**: Doble clic en `instalar.bat` (como administrador)
2. **Usar aplicación**: Doble clic en "Site Survey App.bat" del escritorio

## Instalación Manual

1. Copia `SiteSurveyApp.exe` al escritorio
2. Ejecuta directamente el archivo .exe

## ⚠️ Notas Importantes

- **Antivirus**: Windows Defender puede bloquear la aplicación
- **Puerto**: La app usa puerto 5000 (cerrar otras apps si hay conflicto)
- **Administrador**: Ejecutar como administrador si hay problemas

## 🔧 Solución de Problemas

### La app no se abre
1. Verificar que Windows Defender no la bloquee
2. Ejecutar como administrador
3. Verificar puerto 5000 libre

### Error de puerto
1. Abrir CMD como administrador
2. Ejecutar: `netstat -ano | findstr :5000`
3. Terminar proceso que use puerto 5000

## 📞 Soporte

- **Desarrollador**: Efrén Alexis Hernández
- **Empresa**: FANGIO COM
- **Versión**: 1.0

---
*Instalación completada: {datetime.now().strftime("%d/%m/%Y %H:%M")}*
'''
    
    with open(os.path.join(dist_folder, 'README_INSTALACION.txt'), 'w', encoding='utf-8') as f:
        f.write(readme)
    print("✅ README_INSTALACION.txt creado")
    
    # Crear ZIP
    zip_filename = f"SiteSurveyApp_Distribucion_{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dist_folder)
                zipf.write(file_path, arcname)
    
    print(f"📦 ZIP creado: {zip_filename}")
    
    # Mostrar resumen
    print()
    print("=" * 60)
    print("    ✅ PAQUETE CREADO EXITOSAMENTE")
    print("=" * 60)
    print()
    print("📁 Archivos incluidos:")
    print("   - SiteSurveyApp.exe (ejecutable principal)")
    print("   - instalar.bat (instalador automático)")
    print("   - README_INSTALACION.txt (instrucciones)")
    print()
    print(f"📦 Archivo ZIP: {zip_filename}")
    print()
    print("🚀 Para distribuir:")
    print("   1. Envía el archivo ZIP por email/Drive")
    print("   2. El equipo extrae y ejecuta instalar.bat")
    print("   3. ¡Listo para usar!")
    print()
    print("💡 Tamaño del paquete:", f"{os.path.getsize(zip_filename) / (1024*1024):.1f} MB")

if __name__ == "__main__":
    main() 