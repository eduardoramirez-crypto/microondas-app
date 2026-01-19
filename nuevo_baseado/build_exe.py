import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_exe():
    """
    Script para convertir la aplicación Flask en un archivo .exe
    usando PyInstaller con todas las carpetas y archivos necesarios
    """
    
    print("=== COMPILANDO APLICACIÓN FLASK A .EXE ===")
    
    # 1. Verificar que PyInstaller esté instalado
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller no está instalado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 2. Crear el archivo spec personalizado
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Archivos y carpetas a incluir
added_files = [
    ('templates', 'templates'),
    ('static', 'static'),
    ('site_survey', 'site_survey'),
    ('Temp', 'Temp'),
    ('uploads', 'uploads'),
    ('llenado-automatico.html', '.'),
    ('base de datos.xlsx', '.'),
    ('EJEMPLO SS VACIO.xlsx', '.'),
]

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'flask',
        'pandas',
        'xlwings',
        'openpyxl',
        'docx',
        'matplotlib',
        'numpy',
        'werkzeug',
        'jinja2',
        'win32com.client',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'markupsafe',
        'itsdangerous',
        'click',
        'blinker',
        'colorama',
        'pyreadline3',
        'xlwings.pro',
        'xlwings.utils',
        'xlwings.constants',
        'xlwings._xlwindows',
        'xlwings._xlmac',
        'xlwings._xlmac_office',
        'xlwings._xlmac_office_2016',
        'xlwings._xlmac_office_2019',
        'xlwings._xlmac_office_365',
        'xlwings._xlmac_office_standalone',
        'xlwings._xlmac_office_standalone_2016',
        'xlwings._xlmac_office_standalone_2019',
        'xlwings._xlmac_office_standalone_365',
        'xlwings._xlmac_office_standalone_2016_32',
        'xlwings._xlmac_office_standalone_2019_32',
        'xlwings._xlmac_office_standalone_365_32',
        'xlwings._xlmac_office_standalone_2016_64',
        'xlwings._xlmac_office_standalone_2019_64',
        'xlwings._xlmac_office_standalone_365_64',
        'xlwings._xlmac_office_standalone_2016_32_64',
        'xlwings._xlmac_office_standalone_2019_32_64',
        'xlwings._xlmac_office_standalone_365_32_64',
        'xlwings._xlmac_office_standalone_2016_64_32',
        'xlwings._xlmac_office_standalone_2019_64_32',
        'xlwings._xlmac_office_standalone_365_64_32',
        'xlwings._xlmac_office_standalone_2016_32_64_32',
        'xlwings._xlmac_office_standalone_2019_32_64_32',
        'xlwings._xlmac_office_standalone_365_32_64_32',
        'xlwings._xlmac_office_standalone_2016_64_32_64',
        'xlwings._xlmac_office_standalone_2019_64_32_64',
        'xlwings._xlmac_office_standalone_365_64_32_64',
        'xlwings._xlmac_office_standalone_2016_32_64_32_64',
        'xlwings._xlmac_office_standalone_2019_32_64_32_64',
        'xlwings._xlmac_office_standalone_365_32_64_32_64',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FANGIO_TELECOM_APP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='static/images/fangio-logo.ico' if os.path.exists('static/images/fangio-logo.ico') else None,
)
'''
    
    # Guardar el archivo spec
    with open('FANGIO_TELECOM_APP.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Archivo .spec creado")
    
    # 3. Crear carpeta de salida
    output_dir = "dist"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    print("✅ Carpeta de salida creada")
    
    # 4. Ejecutar PyInstaller
    print("🔄 Compilando aplicación...")
    cmd = [
        'pyinstaller',
        '--clean',
        '--onefile',
        '--windowed',
        '--name=FANGIO_TELECOM_APP',
        '--add-data=templates;templates',
        '--add-data=static;static',
        '--add-data=site_survey;site_survey',
        '--add-data=Temp;Temp',
        '--add-data=uploads;uploads',
        '--add-data=llenado-automatico.html;.',
        '--add-data=base de datos.xlsx;.',
        '--add-data=EJEMPLO SS VACIO.xlsx;.',
        '--hidden-import=flask',
        '--hidden-import=pandas',
        '--hidden-import=xlwings',
        '--hidden-import=openpyxl',
        '--hidden-import=docx',
        '--hidden-import=matplotlib',
        '--hidden-import=numpy',
        '--hidden-import=werkzeug',
        '--hidden-import=jinja2',
        '--hidden-import=win32com.client',
        '--hidden-import=requests',
        '--hidden-import=urllib3',
        '--hidden-import=certifi',
        '--hidden-import=charset_normalizer',
        '--hidden-import=idna',
        '--hidden-import=markupsafe',
        '--hidden-import=itsdangerous',
        '--hidden-import=click',
        '--hidden-import=blinker',
        '--hidden-import=colorama',
        '--hidden-import=pyreadline3',
        'app.py'
    ]
    
    # Agregar icono si existe
    if os.path.exists('static/images/fangio-logo.ico'):
        cmd.extend(['--icon=static/images/fangio-logo.ico'])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Compilación exitosa!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Error en la compilación:")
        print(e.stderr)
        return False
    
    # 5. Crear archivo de inicio
    create_launcher()
    
    # 6. Crear README
    create_readme()
    
    print("\n🎉 ¡Compilación completada!")
    print(f"📁 El archivo .exe se encuentra en: {output_dir}/FANGIO_TELECOM_APP.exe")
    print("🚀 Puedes ejecutar el archivo directamente")
    
    return True

def create_launcher():
    """Crear un archivo de inicio para el .exe"""
    launcher_content = '''@echo off
title FANGIO TELECOM - Iniciando Aplicación
echo ========================================
echo    FANGIO TELECOM - SISTEMA DE LLENADO
echo ========================================
echo.
echo Iniciando aplicación...
echo.
echo Si el navegador no se abre automáticamente,
echo ve a: http://localhost:5000
echo.
echo Presiona Ctrl+C para cerrar la aplicación
echo.
pause
'''
    
    with open('dist/INICIAR_APLICACION.bat', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("✅ Archivo de inicio creado")

def create_readme():
    """Crear archivo README con instrucciones"""
    readme_content = '''# FANGIO TELECOM - Sistema de Llenado Automático

## 📋 Descripción
Aplicación para el llenado automático de documentos Excel con datos de Google Sheets y archivos subidos por el usuario.

## 🚀 Instalación y Uso

### Requisitos del Sistema:
- Windows 10 o superior
- Microsoft Excel instalado
- Conexión a internet (para Google Sheets)

### Instrucciones de Uso:

1. **Ejecutar la aplicación:**
   - Doble clic en `FANGIO_TELECOM_APP.exe`
   - O ejecutar `INICIAR_APLICACION.bat`

2. **Acceder a la aplicación:**
   - Se abrirá automáticamente en tu navegador
   - URL: http://localhost:5000

3. **Funcionalidades disponibles:**
   - **Site Survey:** Llenado de formularios de sitio
   - **Diseño de Solución:** Llenado de documentos de diseño
   - **Reporte de Planeación:** Generación de reportes
   - **Formulario de Archivos:** Subida de archivos múltiples

## 📁 Estructura de Archivos

```
FANGIO_TELECOM_APP/
├── FANGIO_TELECOM_APP.exe          # Aplicación principal
├── INICIAR_APLICACION.bat          # Script de inicio
├── templates/                      # Plantillas HTML
├── static/                         # Archivos estáticos (CSS, JS, imágenes)
├── uploads/                        # Archivos subidos por usuarios
├── site_survey/                    # Archivos de site survey
├── Temp/                          # Archivos temporales
├── base de datos.xlsx             # Base de datos local
└── EJEMPLO SS VACIO.xlsx          # Plantilla de ejemplo
```

## 🔧 Solución de Problemas

### La aplicación no inicia:
1. Verificar que Excel esté instalado
2. Ejecutar como administrador
3. Verificar antivirus (puede bloquear la ejecución)

### Error de conexión:
1. Verificar conexión a internet
2. Verificar acceso a Google Sheets
3. Revisar firewall

### Archivos no se guardan:
1. Verificar permisos de escritura en la carpeta
2. Verificar que Excel no esté abierto
3. Verificar espacio en disco

## 📞 Soporte
Para soporte técnico, contactar al equipo de desarrollo.

---
**Desarrollado por FANGIO TELECOM**
'''
    
    with open('dist/README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Archivo README creado")

def create_requirements():
    """Crear archivo requirements.txt"""
    requirements = '''flask==2.3.3
pandas==2.0.3
xlwings==0.30.12
openpyxl==3.1.2
python-docx==0.8.11
matplotlib==3.7.2
numpy==1.24.3
requests==2.31.0
pywin32==306
Werkzeug==2.3.7
Jinja2==3.1.2
'''
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print("✅ Archivo requirements.txt creado")

if __name__ == "__main__":
    print("🔧 Configurando compilación...")
    
    # Crear requirements.txt
    create_requirements()
    
    # Instalar dependencias si es necesario
    print("📦 Verificando dependencias...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencias instaladas")
    except subprocess.CalledProcessError:
        print("⚠️  Algunas dependencias no se pudieron instalar automáticamente")
    
    # Compilar
    success = create_exe()
    
    if success:
        print("\n🎯 ¡Compilación exitosa!")
        print("📂 Revisa la carpeta 'dist' para encontrar tu aplicación")
    else:
        print("\n❌ Error en la compilación")
        print("🔍 Revisa los mensajes de error arriba") 