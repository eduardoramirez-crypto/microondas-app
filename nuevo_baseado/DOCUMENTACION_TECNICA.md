# 📚 Documentación Técnica - FANGIO TELECOM

## 🎯 **Descripción General**

FANGIO TELECOM es una aplicación web desarrollada en Flask que gestiona la generación y descarga de documentos técnicos para proyectos de telecomunicaciones. La aplicación maneja dos tipos principales de documentos:

1. **Site Survey** - Encuestas del sitio
2. **Diseño de Solución** - Documentos técnicos de diseño

## 🏗️ **Arquitectura del Sistema**

### **Stack Tecnológico**
- **Backend:** Python 3.7+ con Flask
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Base de Datos:** Google Sheets (CSV)
- **Manejo de Archivos:** xlwings, openpyxl
- **Sistema Operativo:** Windows (principal), Linux/Mac (limitado)

### **Estructura de Directorios**
```
nuevo_baseado/
├── app.py                          # Aplicación principal Flask
├── static/                         # Archivos estáticos
│   ├── images/                     # Imágenes del sistema
│   └── plantillas/                 # Plantillas Excel
├── templates/                      # Plantillas HTML
├── site_survey/                    # Archivos de site survey
├── ptmp_site_survey/              # Archivos PtMP
├── Temp/plantillas/               # Plantillas de diseño
├── archivos_generados/            # Archivos generados por el sistema
├── uploads/                       # Archivos subidos por usuarios
├── logs/                          # Logs del sistema
└── tests/                         # Tests automatizados
```

## 🔧 **Funcionalidades Principales**

### **1. Gestión de Site Survey**
- **Endpoint:** `/redirigir_tipo_llenado` (POST)
- **Plantilla:** `EJEMPLO SS VACIO.xlsx`
- **Funcionalidad:** Genera archivos de encuesta del sitio
- **Archivos generados:** `ss_{user_id}.xlsx`

### **2. Gestión de Diseño de Solución**
- **Endpoint:** `/generar_diseno_solucion` (POST)
- **Plantilla:** `llenadoauto.xlsx`
- **Funcionalidad:** Genera archivos de diseño técnico
- **Archivos generados:** `ds_diseno_solucion_{user_id}_{timestamp}.xlsx`

### **3. Descarga de Archivos**
- **Endpoint:** `/descargar_diseno_solucion` (GET)
- **Funcionalidad:** Descarga archivos generados
- **Validación:** Solo archivos con prefijo `ds_`

### **4. Gestión de Imágenes**
- **Endpoint:** `/ver_imagenes_diseno_solucion` (GET)
- **Funcionalidad:** Visualiza imágenes subidas por categoría
- **Categorías:** electricas, planos_a, fotos_a, kmz, documentos

## 🔐 **Sistema de Seguridad**

### **Validación de Entrada**
```python
def validate_user_input(user_id: str, fila_idx: str) -> tuple[bool, str, Optional[int]]:
    """
    Valida los parámetros de entrada del usuario
    
    Args:
        user_id: ID del usuario (mínimo 3 caracteres)
        fila_idx: Índice de la fila (número entero >= 0)
        
    Returns:
        tuple: (es_valido, mensaje_error, fila_idx_int)
    """
```

### **Manejo de Errores**
- **Decorador:** `@error_handler`
- **Logging:** Automático de todos los errores
- **Respuestas:** Estructuradas en JSON o HTML según el contexto

## 📊 **Sistema de Logging**

### **Configuración**
```python
def setup_logging():
    """
    Configura el sistema de logging para la aplicación
    
    - Nivel: INFO
    - Archivo: logs/fangio_app_YYYYMMDD.log
    - Consola: Salida estándar
    - Formato: timestamp - logger - level - message
    """
```

### **Operaciones Registradas**
- Generación de archivos
- Descargas
- Errores del sistema
- Operaciones de usuario
- Validaciones fallidas

## 🧪 **Sistema de Testing**

### **Estructura de Tests**
```python
class TestFangioApp(unittest.TestCase):
    """Tests para la aplicación principal"""
    
    def test_validate_user_input_valid(self):
        """Test de validación de entrada válida"""
    
    def test_validate_user_input_invalid_user_id(self):
        """Test de validación con user_id inválido"""
    
    def test_validate_user_input_invalid_fila_idx(self):
        """Test de validación con fila_idx inválido"""
```

### **Ejecución de Tests**
```bash
# Ejecutar todos los tests
python test_app.py

# Ejecutar tests específicos
python -m unittest test_app.TestFangioApp.test_validate_user_input_valid
```

## 📡 **APIs y Endpoints**

### **Endpoints Principales**

#### **POST /generar_diseno_solucion**
```json
{
    "user_id": "5140066159E",
    "fila_idx": "4"
}
```

**Respuesta de éxito:**
```json
{
    "success": true,
    "message": "Archivo de DISEÑO DE SOLUCIÓN generado exitosamente",
    "archivo": "ds_diseno_solucion_5140066159E_20250813_120000.xlsx",
    "ruta": "/path/to/file.xlsx"
}
```

**Respuesta de error:**
```json
{
    "success": false,
    "message": "Error específico del sistema",
    "error": "Descripción técnica del error",
    "function": "nombre_funcion",
    "timestamp": "2025-08-13T12:00:00"
}
```

#### **GET /descargar_diseno_solucion**
**Parámetros:**
- `user_id`: ID del usuario
- `fila_idx`: Índice de la fila

**Respuesta:** Archivo Excel para descarga

#### **GET /ver_imagenes_diseno_solucion**
**Parámetros:**
- `user_id`: ID del usuario
- `fila_idx`: Índice de la fila

**Respuesta:** Página HTML con visualizador de imágenes

## 🗄️ **Manejo de Archivos**

### **Tipos de Archivos Soportados**
- **Excel:** `.xlsx` (generación y lectura)
- **Imágenes:** `.jpg`, `.png`, `.gif` (visualización)
- **Documentos:** `.pdf`, `.doc`, `.docx` (almacenamiento)
- **Comprimidos:** `.zip`, `.rar` (almacenamiento)

### **Estructura de Almacenamiento**
```
uploads/
├── electricas/{user_id}/           # Imágenes eléctricas
├── planos_a/{user_id}/             # Planos del sitio A
├── planos_b/{user_id}/             # Planos del sitio B
├── fotos_a/{user_id}/              # Fotos del sitio A
├── fotos_b/{user_id}/              # Fotos del sitio B
├── kmz/{user_id}/                  # Archivos KMZ
└── documentos/{user_id}/           # Documentos adicionales
```

## 🔄 **Flujo de Trabajo**

### **1. Generación de Diseño de Solución**
```
Usuario → Botón "Guardar Archivo" → POST /generar_diseno_solucion
→ Validación de entrada → Lectura Google Sheets → Apertura plantilla
→ Llenado de datos → Guardado → Respuesta de éxito
```

### **2. Descarga de Archivo**
```
Usuario → Botón "Descargar Archivo" → GET /descargar_diseno_solucion
→ Validación de entrada → Búsqueda de archivo → Verificación de existencia
→ Envío del archivo → Descarga en navegador
```

### **3. Visualización de Imágenes**
```
Usuario → Botón "Ver Imágenes" → GET /ver_imagenes_diseno_solucion
→ Escaneo de directorios → Categorización de imágenes → Generación HTML
→ Visualización con modal → Navegación por categorías
```

## 🚨 **Manejo de Errores**

### **Tipos de Errores**
1. **Errores de Validación:** Entrada de usuario inválida
2. **Errores de Archivo:** Plantillas no encontradas
3. **Errores de Excel:** Problemas con xlwings
4. **Errores de Red:** Problemas con Google Sheets
5. **Errores del Sistema:** Excepciones no manejadas

### **Estrategias de Recuperación**
- **Reintentos automáticos** para operaciones de Excel
- **Fallbacks** para plantillas no encontradas
- **Logging detallado** para debugging
- **Respuestas de error estructuradas** para el frontend

## 📈 **Métricas y Monitoreo**

### **Métricas Registradas**
- Tiempo de generación de archivos
- Tamaño de archivos generados
- Frecuencia de uso por usuario
- Errores por tipo y función
- Rendimiento del sistema

### **Logs de Auditoría**
- Operaciones realizadas por usuario
- Archivos generados y descargados
- Cambios en la configuración
- Accesos al sistema

## 🔧 **Configuración del Sistema**

### **Variables de Entorno**
```python
GOOGLE_SHEETS_CSV_URL = 'https://docs.google.com/spreadsheets/d/.../export?format=csv'
FLASK_ENV = 'development'  # o 'production'
LOG_LEVEL = 'INFO'         # DEBUG, INFO, WARNING, ERROR
```

### **Configuración de Logging**
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/fangio_app_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

## 🚀 **Despliegue y Mantenimiento**

### **Requisitos del Sistema**
- **Python:** 3.7 o superior
- **Memoria:** Mínimo 4GB RAM
- **Almacenamiento:** 10GB espacio libre
- **Sistema Operativo:** Windows 10+ (recomendado)

### **Dependencias Principales**
```
Flask>=2.0.0
pandas>=1.3.0
xlwings>=0.27.0
openpyxl>=3.0.0
```

### **Comandos de Mantenimiento**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
python test_app.py

# Verificar logs
tail -f logs/fangio_app_$(date +%Y%m%d).log

# Limpiar archivos temporales
python -c "import shutil; shutil.rmtree('Temp', ignore_errors=True)"
```

## 🔮 **Roadmap y Mejoras Futuras**

### **Corto Plazo (1-2 meses)**
- [ ] Implementar autenticación de usuarios
- [ ] Agregar sistema de caché para Google Sheets
- [ ] Mejorar validación de archivos subidos
- [ ] Implementar compresión de archivos

### **Mediano Plazo (3-6 meses)**
- [ ] Migrar a base de datos PostgreSQL
- [ ] Implementar API REST completa
- [ ] Agregar sistema de notificaciones
- [ ] Implementar backup automático

### **Largo Plazo (6+ meses)**
- [ ] Migrar a arquitectura microservicios
- [ ] Implementar machine learning para análisis
- [ ] Agregar dashboard de analytics
- [ ] Implementar CI/CD pipeline

## 📞 **Soporte y Contacto**

### **Equipo de Desarrollo**
- **Desarrollador Principal:** [Nombre]
- **Arquitecto de Sistemas:** [Nombre]
- **QA Engineer:** [Nombre]

### **Canales de Soporte**
- **Email:** soporte@fangio-telecom.com
- **Documentación:** [URL del wiki]
- **Issues:** [URL del repositorio]
- **Chat:** [URL del Slack/Discord]

---

**Última actualización:** 13 de Agosto, 2025  
**Versión del documento:** 1.0.0  
**Estado:** En desarrollo activo
