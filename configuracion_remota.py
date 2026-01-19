#!/usr/bin/env python3
"""
Configurador de Acceso Remoto - Fangio Telecom
Permite acceso desde CDMX a la aplicación en Guadalajara
"""

import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def verificar_ngrok():
    """Verifica si ngrok está instalado"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ngrok encontrado")
            return True
    except FileNotFoundError:
        print("❌ ngrok no encontrado")
        return False

def descargar_ngrok():
    """Descarga e instala ngrok"""
    print("📥 Descargando ngrok...")
    
    # URL de descarga de ngrok
    ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
    
    try:
        import urllib.request
        import zipfile
        
        # Descargar ngrok
        print("Descargando desde:", ngrok_url)
        urllib.request.urlretrieve(ngrok_url, "ngrok.zip")
        
        # Extraer
        with zipfile.ZipFile("ngrok.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Limpiar
        os.remove("ngrok.zip")
        
        print("✅ ngrok instalado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error descargando ngrok: {e}")
        print("Por favor descarga manualmente desde: https://ngrok.com/download")
        return False

def iniciar_aplicacion():
    """Inicia la aplicación Flask"""
    print("🚀 Iniciando aplicación Flask...")
    
    try:
        # Cambiar al directorio de la aplicación
        os.chdir("nuevo_baseado")
        
        # Iniciar Flask en segundo plano
        process = subprocess.Popen([
            sys.executable, "run_app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar un poco para que Flask inicie
        time.sleep(3)
        
        print("✅ Aplicación Flask iniciada")
        return process
        
    except Exception as e:
        print(f"❌ Error iniciando Flask: {e}")
        return None

def iniciar_ngrok():
    """Inicia ngrok para acceso remoto"""
    print("🌐 Iniciando ngrok para acceso remoto...")
    
    try:
        # Iniciar ngrok
        ngrok_process = subprocess.Popen([
            "ngrok", "http", "5000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar a que ngrok se inicie
        time.sleep(5)
        
        # Obtener URL pública
        try:
            import requests
            response = requests.get("http://localhost:4040/api/tunnels")
            tunnels = response.json()["tunnels"]
            
            if tunnels:
                public_url = tunnels[0]["public_url"]
                print(f"✅ URL pública: {public_url}")
                return ngrok_process, public_url
            else:
                print("❌ No se pudo obtener URL pública")
                return ngrok_process, None
                
        except Exception as e:
            print(f"⚠️ No se pudo obtener URL automáticamente: {e}")
            print("Revisa la interfaz de ngrok en: http://localhost:4040")
            return ngrok_process, None
            
    except Exception as e:
        print(f"❌ Error iniciando ngrok: {e}")
        return None, None

def mostrar_instrucciones(public_url=None):
    """Muestra instrucciones de uso"""
    print("\n" + "="*50)
    print("    CONFIGURACIÓN COMPLETADA")
    print("="*50)
    
    print("\n📋 INSTRUCCIONES:")
    print("1. La aplicación está ejecutándose localmente")
    print("2. Acceso local: http://127.0.0.1:5000")
    
    if public_url:
        print(f"3. Acceso remoto (CDMX): {public_url}")
        print("4. Comparte esta URL con tu equipo en Guadalajara")
    
    print("\n🔧 CONFIGURACIÓN:")
    print("- Puerto local: 5000")
    print("- Interfaz ngrok: http://localhost:4040")
    print("- Logs de ngrok: Revisa la terminal de ngrok")
    
    print("\n⚠️ IMPORTANTE:")
    print("- Esta URL es temporal y cambiará al reiniciar")
    print("- Para acceso permanente, considera un VPS")
    print("- Mantén esta terminal abierta")
    
    print("\n🛑 Para detener:")
    print("- Presiona Ctrl+C en ambas terminales")
    print("- O cierra las ventanas de terminal")

def main():
    """Función principal"""
    print("🚀 Configurador de Acceso Remoto - Fangio Telecom")
    print("="*50)
    
    # Verificar ngrok
    if not verificar_ngrok():
        print("\n¿Deseas descargar ngrok automáticamente? (s/n): ", end="")
        respuesta = input().lower()
        
        if respuesta == 's':
            if not descargar_ngrok():
                return
        else:
            print("Por favor instala ngrok manualmente desde: https://ngrok.com/download")
            return
    
    # Iniciar aplicación Flask
    flask_process = iniciar_aplicacion()
    if not flask_process:
        return
    
    # Iniciar ngrok
    ngrok_process, public_url = iniciar_ngrok()
    if not ngrok_process:
        print("❌ No se pudo iniciar ngrok")
        flask_process.terminate()
        return
    
    # Mostrar instrucciones
    mostrar_instrucciones(public_url)
    
    # Abrir navegador
    if public_url:
        print(f"\n🌐 Abriendo navegador en: {public_url}")
        webbrowser.open(public_url)
    
    try:
        # Mantener ejecutándose
        print("\n⏳ Presiona Ctrl+C para detener...")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servicios...")
        
        # Terminar procesos
        if flask_process:
            flask_process.terminate()
        if ngrok_process:
            ngrok_process.terminate()
        
        print("✅ Servicios detenidos")

if __name__ == "__main__":
    main() 