# --- VERSIÓN SIMPLIFICADA CON BOTONES DIRECTOS ---
# Sin dependencias complejas, solo Flask básico
# --- FIN DEL COMENTARIO ---

from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
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
                    <a href="/login.html" class="btn btn-login">
                        <div class="btn-icon">🔐</div>
                        <div>Login Fangio</div>
                        <small>Acceso Directo</small>
                    </a>
                    <a href="/ptpFangio.html" class="btn btn-ptp">
                        <div class="btn-icon">📡</div>
                        <div>PTP Fangio</div>
                        <small>Acceso Directo</small>
                    </a>
                    <a href="/ptmpFangio.html" class="btn btn-ptmp">
                        <div class="btn-icon">🌐</div>
                        <div>PTMP Fangio</div>
                        <small>Acceso Directo</small>
                    </a>
                    <a href="/llenado-automatico.html" class="btn btn-llenado">
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

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("🚀 Iniciando aplicación simplificada...")
    print("🎯 Acceso directo habilitado - Sin autenticación requerida")
    print("📱 Ve a: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True) 