# --- VERSIÓN CON BOTÓN DIRECTO A LOGIN FANGIO ---
# Incluye botón para acceso directo sin autenticación
# --- FIN DEL COMENTARIO ---

import os
import time
import pandas as pd
import xlwings as xw
import win32com.client
from flask import Flask, request, send_file, render_template_string, redirect, url_for, after_this_request, jsonify, session, send_from_directory
from werkzeug.utils import secure_filename
import sys
import re
import dataframe_image as dfi
import matplotlib.pyplot as plt
import textwrap
import unicodedata
import glob
import subprocess
import threading
import psutil
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'fangio_telecom_2025'  # Clave secreta para sesiones

# Configuración para múltiples usuarios
MAX_CONCURRENT_USERS = 10
EXCEL_TIMEOUT = 30  # segundos
SESSION_TIMEOUT = 3600  # 1 hora

# Diccionario para rastrear sesiones activas
active_sessions = {}
excel_processes = {}

def normaliza_na(valor):
    if isinstance(valor, str) and valor.strip().lower() == "n/a":
        return "N/A"
    elif pd.isna(valor):
        return "N/A"
    elif valor == "" or (isinstance(valor, str) and valor.strip() == ""):
        return "N/A"
    return valor

def normaliza_texto(texto):
    if pd.isna(texto):
        return ""
    texto_str = str(texto).strip()
    if texto_str == "" or texto_str.lower() == "nan":
        return ""
    return texto_str

# Función mejorada para cerrar procesos Excel
def cerrar_procesos_excel_mejorado():
    try:
        # Buscar todos los procesos de Excel
        excel_processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'excel' in proc.info['name'].lower():
                    excel_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Cerrar procesos de Excel de forma más agresiva
        for proc in excel_processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)  # Esperar hasta 5 segundos
            except psutil.TimeoutExpired:
                try:
                    proc.kill()  # Forzar cierre si no responde
                except:
                    pass
            except:
                pass
        
        # Limpiar procesos de xlwings
        try:
            xw.apps.kill()
        except:
            pass
            
        return True
    except Exception as e:
        print(f"Error al cerrar procesos Excel: {e}")
        return False

# Función para limpiar sesiones expiradas
def limpiar_sesiones_expiradas():
    current_time = datetime.now()
    expired_sessions = []
    
    for session_id, session_data in active_sessions.items():
        if current_time - session_data['created'] > timedelta(seconds=SESSION_TIMEOUT):
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        del active_sessions[session_id]

# Función para verificar límite de usuarios
def verificar_limite_usuarios():
    limpiar_sesiones_expiradas()
    return len(active_sessions) < MAX_CONCURRENT_USERS

# Función para crear sesión de usuario
def crear_sesion_usuario():
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = {
        'created': datetime.now(),
        'last_activity': datetime.now(),
        'excel_processes': []
    }
    return session_id

# Función para actualizar actividad de sesión
def actualizar_actividad_sesion(session_id):
    if session_id in active_sessions:
        active_sessions[session_id]['last_activity'] = datetime.now()

# Función para cerrar sesión
def cerrar_sesion_usuario(session_id):
    if session_id in active_sessions:
        # Cerrar procesos Excel asociados a esta sesión
        for proc_id in active_sessions[session_id]['excel_processes']:
            try:
                if proc_id in excel_processes:
                    del excel_processes[proc_id]
            except:
                pass
        del active_sessions[session_id]

# Obtener el directorio base de la aplicación
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

print(f"Directorio base: {base_dir}")
print("Archivos en el directorio:", os.listdir(base_dir))

# Buscar el archivo en múltiples ubicaciones
llenado_paths = [
    os.path.join(base_dir, 'llenado-automatico.html'),
    os.path.join(base_dir, 'static', 'llenado-automatico.html'),
    os.path.join(base_dir, 'templates', 'llenado-automatico.html'),
    'llenado-automatico.html'  # Directorio actual como fallback
]

html_form = None
for path in llenado_paths:
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                html_form = f.read()
            print(f"Archivo llenado-automatico.html encontrado en: {path}")
            break
    except Exception as e:
        print(f"Error al leer {path}: {e}")
        continue

if html_form is None:
    print("ADVERTENCIA: No se pudo encontrar llenado-automatico.html")
    html_form = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Llenado Automático - Fangio Telecom</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .error { color: red; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏢 Fangio Telecom - Sistema de Gestión</h1>
            <div class="error">
                <h2>⚠️ Error de Configuración</h2>
                <p>No se pudo cargar el formulario de llenado automático.</p>
                <p>Por favor, contacte al administrador del sistema.</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/')
def index():
    # Verificar límite de usuarios
    if not verificar_limite_usuarios():
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sistema Ocupado - Fangio Telecom</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
                h1 { color: #e74c3c; }
                .btn { background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚫 Sistema Ocupado</h1>
                <p>El sistema está siendo utilizado por demasiados usuarios simultáneos.</p>
                <p>Por favor, intente nuevamente en unos minutos.</p>
                <a href="/" class="btn">Reintentar</a>
            </div>
        </body>
        </html>
        """)
    
    # Crear sesión para el usuario
    session_id = crear_sesion_usuario()
    session['session_id'] = session_id
    
    # Crear página de inicio con botones directos
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fangio Telecom - Acceso Directo</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 {
                margin: 0;
                font-size: 2.5em;
                font-weight: 300;
            }
            .content {
                padding: 40px;
            }
            .buttons-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .btn {
                background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                color: white;
                border: none;
                padding: 20px;
                border-radius: 10px;
                cursor: pointer;
                text-decoration: none;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                font-weight: 600;
                font-size: 1.1em;
                min-height: 120px;
            }
            .btn:hover {
                background: linear-gradient(135deg, #2980b9 0%, #1f5f8b 100%);
                transform: translateY(-3px);
                box-shadow: 0 8px 15px rgba(0,0,0,0.2);
            }
            .btn-login {
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            }
            .btn-login:hover {
                background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
            }
            .btn-ptp {
                background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            }
            .btn-ptp:hover {
                background: linear-gradient(135deg, #c0392b 0%, #a93226 100%);
            }
            .btn-ptmp {
                background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            }
            .btn-ptmp:hover {
                background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
            }
            .btn-llenado {
                background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            }
            .btn-llenado:hover {
                background: linear-gradient(135deg, #e67e22 0%, #d35400 100%);
            }
            .btn-icon {
                font-size: 2em;
                margin-bottom: 10px;
            }
            .status-bar {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
                margin-top: 20px;
                text-align: center;
                border-left: 4px solid #3498db;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏢 Fangio Telecom</h1>
                <p>Sistema de Gestión - Acceso Directo</p>
            </div>
            <div class="content">
                <div class="buttons-grid">
                    <a href="/login-directo" class="btn btn-login">
                        <div class="btn-icon">🔐</div>
                        <div>Login Fangio</div>
                        <small>Acceso Directo</small>
                    </a>
                    <a href="/ptpFangio" class="btn btn-ptp">
                        <div class="btn-icon">📡</div>
                        <div>PTP Fangio</div>
                        <small>Acceso Directo</small>
                    </a>
                    <a href="/ptmpFangio" class="btn btn-ptmp">
                        <div class="btn-icon">🌐</div>
                        <div>PTMP Fangio</div>
                        <small>Acceso Directo</small>
                    </a>
                    <a href="/llenado-automatico" class="btn btn-llenado">
                        <div class="btn-icon">📊</div>
                        <div>Llenado Automático</div>
                        <small>Procesar Excel</small>
                    </a>
                </div>
                <div class="status-bar">
                    <strong>✅ Sistema Activo</strong> - Acceso directo habilitado sin autenticación
                </div>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/login-directo')
def login_directo():
    if 'session_id' not in session:
        # Crear sesión automáticamente si no existe
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', 'login.html')

@app.route('/ptpFangio')
def ptp_fangio():
    if 'session_id' not in session:
        # Crear sesión automáticamente si no existe
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', 'ptpFangio.html')

@app.route('/ptmpFangio')
def ptmp_fangio():
    if 'session_id' not in session:
        # Crear sesión automáticamente si no existe
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', 'ptmpFangio.html')

@app.route('/llenado-automatico')
def llenado_automatico():
    if 'session_id' not in session:
        # Crear sesión automáticamente si no existe
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    
    # Buscar archivos Excel en el directorio
    archivos_excel = []
    for archivo in os.listdir(base_dir):
        if archivo.endswith(('.xlsx', '.xls')):
            archivos_excel.append(archivo)
    
    # Modificar el HTML para incluir los archivos encontrados
    html_modificado = html_form
    
    if archivos_excel:
        archivos_html = ""
        for archivo in archivos_excel:
            archivos_html += f'<option value="{archivo}">{archivo}</option>'
        
        # Reemplazar placeholder en el HTML
        html_modificado = html_form.replace('<!-- ARCHIVOS_EXCEL -->', archivos_html)
    
    return render_template_string(html_modificado)

@app.route('/site_survey_checkboxes', methods=['GET'])
def site_survey_checkboxes():
    if 'session_id' not in session:
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', 'site_survey_checkboxes.html')

@app.route('/diseno_solucion', methods=['GET', 'POST'])
def diseno_solucion():
    if 'session_id' not in session:
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', 'formulario_archivos.html')

@app.route('/site_survey', methods=['GET'])
def site_survey():
    if 'session_id' not in session:
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', 'site_survey_checkboxes.html')

@app.route('/seleccion_tipo_llenado')
def seleccion_tipo_llenado():
    if 'session_id' not in session:
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', 'seleccion_tipo_llenado.html')

@app.route('/seleccion_llenado_ptp')
def seleccion_llenado_ptp():
    if 'session_id' not in session:
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', 'seleccion_llenado_ptp.html')

@app.route('/seleccion_llenado_ptmp')
def seleccion_llenado_ptmp():
    if 'session_id' not in session:
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', 'seleccion_llenado_ptmp.html')

@app.route('/subir_imagenes_ptp', methods=['GET', 'POST'])
def subir_imagenes_ptp():
    if 'session_id' not in session:
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', 'subir_imagenes_ptp.html')

@app.route('/subir_imagenes_ptp_planos_b', methods=['GET', 'POST'])
def subir_imagenes_ptp_planos_b():
    if 'session_id' not in session:
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', 'subir_imagenes_ptp_planos_b.html')

@app.route('/subir_imagenes_ptp_fotos_a', methods=['GET', 'POST'])
def subir_imagenes_ptp_fotos_a():
    if 'session_id' not in session:
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', 'subir_imagenes_ptp_fotos_a.html')

@app.route('/subir_imagenes_ptp_fotos_b', methods=['GET', 'POST'])
def subir_imagenes_ptp_fotos_b():
    if 'session_id' not in session:
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', 'subir_imagenes_ptp_fotos_b.html')

@app.route('/logout')
def logout():
    if 'session_id' in session:
        cerrar_sesion_usuario(session['session_id'])
        session.pop('session_id', None)
    return redirect('/')

@app.route('/status')
def status():
    """Endpoint para verificar el estado del sistema"""
    limpiar_sesiones_expiradas()
    return jsonify({
        'active_users': len(active_sessions),
        'max_users': MAX_CONCURRENT_USERS,
        'excel_processes': len(excel_processes),
        'system_healthy': True
    })

@app.route('/<path:filename>')
def serve_file(filename):
    if 'session_id' not in session:
        session_id = crear_sesion_usuario()
        session['session_id'] = session_id
    
    actualizar_actividad_sesion(session['session_id'])
    return send_from_directory('.', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Iniciando aplicación con acceso directo...")
    print(f"📊 Límite de usuarios concurrentes: {MAX_CONCURRENT_USERS}")
    print(f"⏱️  Timeout de sesión: {SESSION_TIMEOUT} segundos")
    print(f"🔧 Timeout de Excel: {EXCEL_TIMEOUT} segundos")
    print(f"🎯 Acceso directo habilitado - Sin autenticación requerida")
    app.run(host='0.0.0.0', port=port, debug=True) 