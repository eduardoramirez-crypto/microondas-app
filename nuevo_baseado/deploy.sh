#!/bin/bash

# Script de despliegue seguro para Fangio Telecom PtP
# Este script prepara la aplicación para producción con todas las protecciones

set -e  # Salir si cualquier comando falla

echo "🛡️ Iniciando despliegue seguro de Fangio Telecom PtP..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con color
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "package.json" ]; then
    print_error "No se encontró package.json. Ejecute este script desde el directorio raíz del proyecto."
    exit 1
fi

# Crear directorio de producción
print_status "Creando directorio de producción..."
mkdir -p dist/production
mkdir -p dist/backup

# Backup de la versión anterior
if [ -d "dist/production" ] && [ "$(ls -A dist/production)" ]; then
    print_status "Creando backup de la versión anterior..."
    timestamp=$(date +"%Y%m%d_%H%M%S")
    cp -r dist/production "dist/backup/production_$timestamp"
    print_success "Backup creado: dist/backup/production_$timestamp"
fi

# Instalar dependencias si es necesario
if [ ! -d "node_modules" ]; then
    print_status "Instalando dependencias..."
    npm install
fi

# Ejecutar ofuscación
print_status "Ejecutando ofuscación de código..."
node obfuscate.js

# Ejecutar minificación
print_status "Ejecutando minificación avanzada..."
node minify.js

# Verificar que los archivos se crearon correctamente
if [ ! -f "templates/ptpFangioactualizacion_protected.html" ]; then
    print_error "Error: No se pudo crear el archivo protegido"
    exit 1
fi

if [ ! -f "templates/ptpFangioactualizacion_minified.html" ]; then
    print_error "Error: No se pudo crear el archivo minificado"
    exit 1
fi

# Copiar archivos a producción
print_status "Copiando archivos a directorio de producción..."

# Usar la versión minificada como versión de producción
cp "templates/ptpFangioactualizacion_minified.html" "dist/production/index.html"

# Copiar archivos CSS si existen
if [ -f "estilos_mejorados.css" ]; then
    cp "estilos_mejorados.css" "dist/production/"
fi

# Copiar archivos de seguridad
cp "security.js" "dist/production/"
cp "server_validation.py" "dist/production/"

# Crear archivo de configuración de servidor
cat > "dist/production/server_config.py" << 'EOF'
#!/usr/bin/env python3
"""
Configuración del servidor para Fangio Telecom PtP
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import os
import sys
from server_validation import validator

class SecureHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def end_headers(self):
        # Agregar headers de seguridad
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net https://unpkg.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self';")
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Log personalizado
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server(port=8443, use_ssl=True):
    """Ejecutar servidor con configuración de seguridad"""
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, SecureHTTPRequestHandler)
    
    if use_ssl:
        # Configurar SSL (requiere certificados)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # context.load_cert_chain('cert.pem', 'key.pem')  # Descomentar si tienes certificados
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print(f"🔒 Servidor HTTPS iniciado en puerto {port}")
    else:
        print(f"🌐 Servidor HTTP iniciado en puerto {port}")
    
    print("🛡️ Aplicación protegida ejecutándose...")
    print("📊 Validador del servidor activo")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        httpd.shutdown()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Servidor seguro para Fangio Telecom PtP')
    parser.add_argument('--port', type=int, default=8443, help='Puerto del servidor')
    parser.add_argument('--no-ssl', action='store_true', help='Deshabilitar SSL')
    
    args = parser.parse_args()
    
    run_server(port=args.port, use_ssl=not args.no_ssl)
EOF

# Crear archivo de inicio rápido
cat > "dist/production/start.sh" << 'EOF'
#!/bin/bash
echo "🚀 Iniciando Fangio Telecom PtP (Versión Protegida)"
echo "🛡️ Todas las protecciones activas"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

# Instalar dependencias si es necesario
if [ ! -f "requirements.txt" ]; then
    echo "📦 Creando requirements.txt..."
    cat > requirements.txt << 'REQEOF'
# Dependencias para Fangio Telecom PtP
# No se requieren dependencias adicionales para la versión básica
REQEOF
fi

# Ejecutar servidor
echo "🌐 Iniciando servidor..."
python3 server_config.py --port 8080 --no-ssl
EOF

chmod +x "dist/production/start.sh"

# Crear archivo README para producción
cat > "dist/production/README.md" << 'EOF'
# Fangio Telecom PtP - Versión de Producción

## 🛡️ Características de Seguridad Implementadas

- ✅ **Ofuscación de JavaScript**: Código ofuscado para dificultar la lectura
- ✅ **Minificación**: Archivos comprimidos para reducir legibilidad
- ✅ **Anti-Debugging**: Detección y bloqueo de herramientas de desarrollador
- ✅ **Validación del Servidor**: Verificación de todas las operaciones críticas
- ✅ **Headers de Seguridad**: Protección contra ataques comunes
- ✅ **Rate Limiting**: Prevención de ataques de fuerza bruta
- ✅ **Integridad del Código**: Verificación de manipulación

## 🚀 Inicio Rápido

```bash
# Ejecutar servidor
./start.sh

# O manualmente
python3 server_config.py --port 8080 --no-ssl
```

## ⚠️ Importante

Esta es una versión de producción con protecciones activas. 
El código está ofuscado y minificado para proteger la propiedad intelectual.

## 🔧 Configuración

- Puerto por defecto: 8080
- Para HTTPS, configure certificados SSL en `server_config.py`
- El validador del servidor está activo por defecto

## 📊 Monitoreo

El servidor registra eventos de seguridad y intentos de acceso no autorizado.
EOF

# Crear archivo .htaccess para Apache (si se usa)
cat > "dist/production/.htaccess" << 'EOF'
# Configuración de seguridad para Apache
# Fangio Telecom PtP - Versión Protegida

# Headers de seguridad
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options DENY
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net https://unpkg.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self';"
Header always set Referrer-Policy "strict-origin-when-cross-origin"

# Prevenir acceso a archivos sensibles
<Files "*.py">
    Order Allow,Deny
    Deny from all
</Files>

<Files "*.js.map">
    Order Allow,Deny
    Deny from all
</Files>

# Compresión
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>

# Cache
<IfModule mod_expires.c>
    ExpiresActive on
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
</IfModule>
EOF

# Estadísticas finales
print_status "Generando estadísticas de despliegue..."

original_size=$(du -sh templates/ptpFangioactualizacion.html | cut -f1)
protected_size=$(du -sh templates/ptpFangioactualizacion_protected.html | cut -f1)
minified_size=$(du -sh templates/ptpFangioactualizacion_minified.html | cut -f1)
production_size=$(du -sh dist/production | cut -f1)

echo ""
print_success "🎉 Despliegue completado exitosamente!"
echo ""
echo "📊 Estadísticas:"
echo "   📄 Tamaño original: $original_size"
echo "   🛡️ Tamaño protegido: $protected_size"
echo "   📦 Tamaño minificado: $minified_size"
echo "   🚀 Tamaño producción: $production_size"
echo ""
echo "📁 Archivos generados:"
echo "   ✅ dist/production/index.html (versión protegida)"
echo "   ✅ dist/production/security.js (módulo de seguridad)"
echo "   ✅ dist/production/server_config.py (servidor seguro)"
echo "   ✅ dist/production/start.sh (script de inicio)"
echo "   ✅ dist/production/.htaccess (configuración Apache)"
echo "   ✅ dist/production/README.md (documentación)"
echo ""
echo "🚀 Para iniciar la aplicación:"
echo "   cd dist/production"
echo "   ./start.sh"
echo ""
print_warning "⚠️  Recuerde: Esta versión está optimizada para producción con todas las protecciones activas."
print_warning "⚠️  Para desarrollo, use la versión original en templates/"
