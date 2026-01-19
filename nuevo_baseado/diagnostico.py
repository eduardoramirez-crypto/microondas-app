#!/usr/bin/env python3
"""
Script de diagnóstico para identificar problemas en la aplicación Flask
"""

import os
import sys
import importlib

def check_python_version():
    """Verifica la versión de Python"""
    print(f"🐍 Python versión: {sys.version}")
    if sys.version_info < (3, 7):
        print("⚠️  Se recomienda Python 3.7 o superior")
    else:
        print("✅ Versión de Python compatible")

def check_dependencies():
    """Verifica las dependencias necesarias"""
    print("\n📦 Verificando dependencias...")
    
    required_packages = [
        'flask',
        'pandas',
        'xlwings',
        'win32com',
        'matplotlib',
        'dataframe_image'
    ]
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NO INSTALADO")
            print(f"   Instalar con: pip install {package}")

def check_directories():
    """Verifica que existan los directorios necesarios"""
    print("\n📁 Verificando directorios...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    required_dirs = [
        'templates',
        'static',
        'site_survey',
        'ptmp_site_survey',
        'uploads',
        'logs'
    ]
    
    for dir_name in required_dirs:
        dir_path = os.path.join(current_dir, dir_name)
        if os.path.exists(dir_path):
            print(f"✅ {dir_name}")
        else:
            print(f"❌ {dir_name} - NO EXISTE")
            try:
                os.makedirs(dir_path, exist_ok=True)
                print(f"   ✅ Creado: {dir_name}")
            except Exception as e:
                print(f"   ❌ Error creando: {e}")

def check_files():
    """Verifica que existan los archivos necesarios"""
    print("\n📄 Verificando archivos...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    required_files = [
        'app.py',
        'templates/index.html',
        'templates/seleccion_tipo_llenado.html'
    ]
    
    for file_name in required_files:
        file_path = os.path.join(current_dir, file_name)
        if os.path.exists(file_path):
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} - NO EXISTE")

def check_network():
    """Verifica la conectividad de red"""
    print("\n🌐 Verificando conectividad...")
    
    try:
        import urllib.request
        import urllib.error
        
        # Probar conexión a Google
        try:
            urllib.request.urlopen('https://www.google.com', timeout=5)
            print("✅ Conexión a Internet: OK")
        except Exception as e:
            print(f"❌ Conexión a Internet: {e}")
        
        # Probar conexión a Google Sheets
        try:
            sheets_url = 'https://docs.google.com/spreadsheets/d/1sfOY1Y3dNVCOT8zyCMzpgARv-R_jRE-S/export?format=csv'
            urllib.request.urlopen(sheets_url, timeout=10)
            print("✅ Conexión a Google Sheets: OK")
        except Exception as e:
            print(f"❌ Conexión a Google Sheets: {e}")
            
    except ImportError:
        print("⚠️  No se puede verificar conectividad (urllib no disponible)")

def main():
    """Función principal de diagnóstico"""
    print("🔍 DIAGNÓSTICO DE LA APLICACIÓN FLASK")
    print("=" * 50)
    
    check_python_version()
    check_dependencies()
    check_directories()
    check_files()
    check_network()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN DEL DIAGNÓSTICO")
    print("Si hay ❌, esos son los problemas que debes resolver.")
    print("Si todo está ✅, la aplicación debería funcionar correctamente.")
    
    print("\n🚀 Para probar la aplicación:")
    print("1. python test_simple.py (prueba básica)")
    print("2. python app.py (aplicación completa)")

if __name__ == '__main__':
    main()
