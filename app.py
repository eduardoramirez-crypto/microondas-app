#!/usr/bin/env python3
"""
Punto de entrada principal para el despliegue en Render/Railway
Redirige a la aplicación principal en nuevo_baseado/
"""

import os
import sys

# Agregar el directorio nuevo_baseado al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'nuevo_baseado'))

# Cambiar al directorio de trabajo correcto
os.chdir(os.path.join(os.path.dirname(__file__), 'nuevo_baseado'))

# Importar y ejecutar la aplicación principal
if __name__ == "__main__":
    from app import app
    import os
    
    # Configuración para producción
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    
    print(f"Iniciando servidor en puerto {port}")
    app.run(debug=False, host=host, port=port, threaded=True)
