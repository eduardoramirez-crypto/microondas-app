#!/usr/bin/env python3
"""
Script para iniciar un servidor local para ptpFangio.html
Esto evita los errores CORS cuando se ejecuta desde archivo local
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def main():
    # Puerto para el servidor
    PORT = 8000
    
    # Obtener el directorio actual
    current_dir = Path.cwd()
    print(f"📁 Directorio actual: {current_dir}")
    
    # Verificar si existe el archivo ptpFangio.html
    html_file = current_dir / "ptpFangio.html"
    if not html_file.exists():
        print("❌ Error: No se encontró ptpFangio.html en el directorio actual")
        print("💡 Asegúrate de ejecutar este script desde la carpeta que contiene ptpFangio.html")
        input("Presiona Enter para salir...")
        return
    
    print(f"✅ Archivo encontrado: {html_file}")
    
    # Cambiar al directorio del archivo
    os.chdir(current_dir)
    
    # Crear el servidor
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"🚀 Servidor iniciado en http://localhost:{PORT}")
            print(f"📂 Sirviendo archivos desde: {current_dir}")
            print(f"🌐 Abriendo navegador automáticamente...")
            print(f"📋 URL completa: http://localhost:{PORT}/ptpFangio.html")
            print("\n" + "="*50)
            print("💡 INSTRUCCIONES:")
            print("1. El navegador se abrirá automáticamente")
            print("2. Si no se abre, ve manualmente a: http://localhost:8000/ptpFangio.html")
            print("3. Ahora las APIs de Google funcionarán sin errores CORS")
            print("4. Para detener el servidor, presiona Ctrl+C")
            print("="*50 + "\n")
            
            # Abrir el navegador automáticamente
            try:
                webbrowser.open(f"http://localhost:{PORT}/ptpFangio.html")
            except:
                print("⚠️ No se pudo abrir el navegador automáticamente")
                print(f"💡 Ve manualmente a: http://localhost:{PORT}/ptpFangio.html")
            
            # Mantener el servidor corriendo
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except OSError as e:
        if e.errno == 48:  # Puerto ya en uso
            print(f"❌ Error: El puerto {PORT} ya está en uso")
            print("💡 Intenta con otro puerto o cierra otras aplicaciones que usen el puerto 8000")
        else:
            print(f"❌ Error al iniciar el servidor: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main() 