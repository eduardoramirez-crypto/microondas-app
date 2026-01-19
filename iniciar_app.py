#!/usr/bin/env python3
"""
Script de inicio para la aplicación FANGIO TELECOM
Este script asegura que la aplicación se ejecute desde el directorio correcto
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    # Obtener la ruta del directorio actual
    current_dir = Path(__file__).parent.absolute()
    
    # Cambiar al directorio nuevo_baseado
    nuevo_baseado_dir = current_dir / "nuevo_baseado"
    
    if not nuevo_baseado_dir.exists():
        print("❌ Error: No se encontró el directorio 'nuevo_baseado'")
        print(f"Directorio actual: {current_dir}")
        input("Presiona Enter para salir...")
        return
    
    # Cambiar al directorio correcto
    os.chdir(nuevo_baseado_dir)
    print(f"✅ Cambiado al directorio: {nuevo_baseado_dir}")
    
    # Verificar que app.py existe
    app_file = nuevo_baseado_dir / "app.py"
    if not app_file.exists():
        print("❌ Error: No se encontró el archivo 'app.py'")
        input("Presiona Enter para salir...")
        return
    
    print("🚀 Iniciando aplicación FANGIO TELECOM...")
    print("📍 URL: http://127.0.0.1:5000")
    print("⏳ Abriendo navegador en 3 segundos...")
    
    # Esperar 3 segundos y abrir el navegador
    time.sleep(3)
    try:
        webbrowser.open('http://127.0.0.1:5000')
        print("🌐 Navegador abierto automáticamente")
    except:
        print("⚠️ No se pudo abrir el navegador automáticamente")
        print("   Abre manualmente: http://127.0.0.1:5000")
    
    print("\n" + "="*50)
    print("🎯 APLICACIÓN INICIADA CORRECTAMENTE")
    print("="*50)
    print("📋 Para detener la aplicación: Ctrl+C")
    print("🔄 Para reiniciar: Ejecuta este script nuevamente")
    print("="*50 + "\n")
    
    # Ejecutar la aplicación Flask
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Aplicación detenida por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar la aplicación: {e}")
        input("Presiona Enter para salir...")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main() 