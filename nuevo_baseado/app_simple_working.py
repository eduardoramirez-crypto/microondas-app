from flask import Flask, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

# Obtener el directorio base
base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)

print(f"🚀 Iniciando aplicación simplificada...")
print(f"📁 Directorio base: {base_dir}")
print(f"📁 Directorio padre: {parent_dir}")

@app.route('/')
def index():
    """Página principal - redirige al llenado automático"""
    return redirect(url_for('llenado_automatico'))

@app.route('/llenado_automatico')
def llenado_automatico():
    """Página de llenado automático"""
    try:
        # Cargar el archivo HTML directamente
        html_path = os.path.join(base_dir, 'llenado-automatico.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error cargando formulario</h1><p>{e}</p>"

@app.route('/ptpFangio')
def ptpFangio():
    """Sirve el archivo ptpFangio.html desde el directorio padre"""
    try:
        return send_from_directory(parent_dir, 'ptpFangio.html')
    except Exception as e:
        return f"<h1>Error</h1><p>Error cargando ptpFangio.html: {e}</p>"

@app.route('/login.html')
def login():
    """Sirve el archivo login.html desde el directorio padre"""
    try:
        return send_from_directory(parent_dir, 'login.html')
    except Exception as e:
        return f"<h1>Error</h1><p>Error cargando login.html: {e}</p>"

@app.route('/estado')
def estado():
    """Página de estado simple"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Estado del Sistema</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .status { padding: 20px; background: #e8f5e8; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>✅ Sistema Funcionando</h1>
        <div class="status">
            <h2>Estado: OPERATIVO</h2>
            <p>La aplicación Flask está funcionando correctamente.</p>
            <ul>
                <li><a href="/">Página Principal</a></li>
                <li><a href="/llenado_automatico">Llenado Automático</a></li>
                <li><a href="/ptpFangio">PTP Fangio</a></li>
                <li><a href="/login.html">Login</a></li>
            </ul>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    print("📱 URL local: http://127.0.0.1:5000")
    print("🌐 URL red: http://192.168.1.22:5000")
    print("📊 Estado: http://127.0.0.1:5000/estado")
    app.run(debug=True, host='0.0.0.0', port=5000) 