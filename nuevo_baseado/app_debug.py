print("🔍 [1/10] Iniciando diagnóstico de app.py...")

print("🔍 [2/10] Importando librerías básicas...")
import os
import sys
print("✅ Librerías básicas importadas")

print("🔍 [3/10] Importando Flask...")
from flask import Flask, request, send_file, render_template_string, redirect, url_for, after_this_request, jsonify, render_template, send_from_directory, session
print("✅ Flask importado")

print("🔍 [4/10] Importando otras librerías...")
import time
import pandas as pd
print("✅ Pandas importado")

print("🔍 [5/10] Importando xlwings...")
try:
    import xlwings as xw
    print("✅ xlwings importado")
except Exception as e:
    print(f"⚠️ Error importando xlwings: {e}")

print("🔍 [6/10] Importando win32com...")
try:
    import win32com.client
    print("✅ win32com importado")
except Exception as e:
    print(f"⚠️ Error importando win32com: {e}")

print("🔍 [7/10] Importando otras librerías...")
import re
import dataframe_image as dfi
import matplotlib.pyplot as plt
import textwrap
import unicodedata
import glob
import subprocess
import threading
import uuid
from datetime import datetime, timedelta
import psutil
print("✅ Todas las librerías importadas")

print("🔍 [8/10] Configurando directorio base...")
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

print(f"✅ Directorio base: {base_dir}")
print(f"✅ Archivos en el directorio: {len(os.listdir(base_dir))} archivos")

print("🔍 [9/10] Cargando archivo llenado-automatico.html...")
llenado_paths = [
    os.path.join(base_dir, 'llenado-automatico.html'),
    os.path.join(base_dir, 'static', 'llenado-automatico.html'),
    os.path.join(base_dir, 'templates', 'llenado-automatico.html'),
    'llenado-automatico.html'
]

html_form = None
for path in llenado_paths:
    try:
        with open(path, encoding='utf-8') as f:
            html_form = f.read()
        print(f"✅ Archivo llenado-automatico.html cargado desde: {path}")
        break
    except Exception as e:
        print(f"❌ No se pudo cargar desde {path}: {e}")
        continue

if html_form is None:
    print("❌ ERROR: No se pudo cargar llenado-automatico.html")
    print("La aplicación se detendrá aquí para evitar problemas")
    input("Presiona Enter para salir...")
    sys.exit(1)

print("🔍 [10/10] Creando aplicación Flask...")
app = Flask(__name__)
app.secret_key = 'fangio_telecom_2024_secure_key'
print("✅ Aplicación Flask creada")

print("🎉 ¡DIAGNÓSTICO COMPLETADO!")
print("La aplicación debería funcionar correctamente ahora.")

@app.route('/')
def index():
    return "✅ Aplicación funcionando correctamente!"

@app.route('/test')
def test():
    return "✅ Ruta de prueba funcionando!"

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    print("📱 URL local: http://127.0.0.1:5000")
    print("🌐 URL red: http://192.168.1.22:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 