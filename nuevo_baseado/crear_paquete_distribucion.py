#!/usr/bin/env python3
"""
Script para crear el paquete de distribución
Autor: Asistente IA
Fecha: 2024
"""

import os
import shutil
import zipfile
from datetime import datetime

def crear_paquete_distribucion():
    """Crea el paquete completo para distribución"""
    
    print("=" * 60)
    print("    CREANDO PAQUETE DE DISTRIBUCIÓN")
    print("    Site Survey App")
    print("=" * 60)
    print()
    
    # Verificar que el ejecutable existe
    if not os.path.exists('dist/SiteSurveyApp.exe'):
        print("❌ Error: No se encontró SiteSurveyApp.exe")
        print("Ejecuta primero: python build_simple.py")
        return False
    
    # Crear carpeta de distribución
    dist_folder = "SiteSurveyApp_Distribucion"
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    
    os.makedirs(dist_folder)
    print(f"📁 Carpeta creada: {dist_folder}")
    
    # Copiar archivos necesarios
    archivos_a_copiar = [
        ('dist/SiteSurveyApp.exe', 'SiteSurveyApp.exe'),
        ('instalar.bat', 'instalar.bat'),
    ]
    
    for origen, destino in archivos_a_copiar:
        if os.path.exists(origen):
            shutil.copy2(origen, os.path.join(dist_folder, destino))
            print(f"✅ Copiado: {destino}")
        else:
            print(f"⚠️ No encontrado: {origen}")
    
    # Crear README de instalación si no existe
    readme_content = '''# 🚀 Site Survey App - Instalación

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
*Instalación completada: {fecha}*
'''.format(fecha=datetime.now().strftime("%d/%m/%Y %H:%M"))
    
    with open(os.path.join(dist_folder, 'README_INSTALACION.txt'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ README_INSTALACION.txt creado")
    
    # Crear archivo de información del sistema
    info_content = f'''Site Survey App - Información del Sistema

Fecha de Creación: {datetime.now().strftime("%d/%m/%Y %H:%M")}
Versión: 1.0
Desarrollador: Efrén Alexis Hernández
Empresa: FANGIO COM

Características:
- Aplicación web local para Site Surveys
- Procesamiento automático de archivos Excel
- Interfaz web intuitiva
- Generación de reportes automáticos
- Soporte para PtP y PtMP

Requisitos:
- Windows 10 o superior
- No requiere Python
- No requiere dependencias adicionales

Tamaño del ejecutable: {os.path.getsize("dist/SiteSurveyApp.exe") / (1024*1024):.1f} MB
'''
    
    with open(os.path.join(dist_folder, 'INFO_SISTEMA.txt'), 'w', encoding='utf-8') as f:
        f.write(info_content)
    print("✅ INFO_SISTEMA.txt creado")
    
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
    print("   - INFO_SISTEMA.txt (información técnica)")
    print()
    print(f"📦 Archivo ZIP: {zip_filename}")
    print()
    print("🚀 Para distribuir:")
    print("   1. Envía el archivo ZIP por email/Drive")
    print("   2. El equipo extrae y ejecuta instalar.bat")
    print("   3. ¡Listo para usar!")
    print()
    print("💡 Tamaño del paquete:", f"{os.path.getsize(zip_filename) / (1024*1024):.1f} MB")
    
    return True

def main():
    """Función principal"""
    try:
        crear_paquete_distribucion()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 