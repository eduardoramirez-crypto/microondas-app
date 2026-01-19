# 🚀 Guía de Implementación - Fangio Telecom

## 📋 **Para el Equipo en Guadalajara**

### **Paso 1: Preparación del Entorno**

#### **Requisitos del Sistema:**
- Windows 10/11
- Python 3.8 o superior
- Navegador web moderno (Chrome, Firefox, Edge)

#### **Instalación de Python:**
1. Descargar Python desde: https://www.python.org/downloads/
2. **IMPORTANTE:** Marcar "Add Python to PATH" durante la instalación
3. Verificar instalación: `python --version`

### **Paso 2: Configuración del Proyecto**

#### **Opción A: Clonar desde GitHub (Recomendado)**
```bash
# 1. Instalar Git
# Descargar desde: https://git-scm.com/download/win

# 2. Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DEL_PROYECTO]

# 3. Instalar dependencias
pip install -r requirements.txt
```

#### **Opción B: Copia Directa de Archivos**
1. Crear carpeta: `Fangio_Telecom_Project`
2. Copiar todos los archivos del proyecto
3. Instalar dependencias manualmente:
```bash
pip install Flask pandas xlwings pywin32 dataframe-image matplotlib
```

### **Paso 3: Configuración de la Aplicación**

#### **Archivos de Configuración:**
1. **API Keys:** Configurar en `config.js`
2. **Rutas de archivos:** Verificar rutas en `app.py`
3. **Base de datos:** Configurar conexiones

#### **Variables de Entorno:**
Crear archivo `.env` en la raíz:
```env
FLASK_ENV=development
FLASK_DEBUG=True
API_KEY_GOOGLE_MAPS=tu_api_key_aqui
```

### **Paso 4: Ejecución de la Aplicación**

#### **Método 1: Ejecutar desde Python**
```bash
cd nuevo_baseado
python run_app.py
```

#### **Método 2: Usar el archivo batch**
```bash
ejecutar_site_survey.bat
```

#### **Método 3: Ejecutar servidor principal**
```bash
python iniciar_servidor.py
```

### **Paso 5: Acceso a la Aplicación**

#### **Local:**
- URL: `http://127.0.0.1:5000`
- URL: `http://localhost:5000`

#### **Red Local:**
- URL: `http://[IP_LOCAL]:5000`
- Ejemplo: `http://192.168.1.100:5000`

## 🔧 **Configuración Avanzada**

### **Para Acceso Remoto (CDMX → Guadalajara):**

#### **Opción 1: ngrok (Temporal)**
```bash
# 1. Descargar ngrok: https://ngrok.com/
# 2. Ejecutar aplicación Flask
python run_app.py

# 3. En otra terminal
ngrok http 5000
# Usar la URL pública generada
```

#### **Opción 2: Servidor VPS (Permanente)**
1. Contratar VPS (DigitalOcean, AWS, etc.)
2. Subir código al servidor
3. Configurar dominio
4. Configurar SSL

#### **Opción 3: Heroku/Railway (PaaS)**
1. Crear cuenta en Heroku/Railway
2. Conectar repositorio GitHub
3. Configurar variables de entorno
4. Deploy automático

## 📁 **Estructura del Proyecto**

```
Fangio_Telecom_Project/
├── 📄 ptpFangio.html          # Página principal PTP
├── 📄 ptmpFangio.html         # Página principal PTMP
├── 📄 login.html              # Página de login
├── 📄 perfil_elevacion.html   # Perfil de elevación
├── 📄 config.js               # Configuración
├── 📄 ejecutar_python.html    # Interfaz Python
├── 📄 ejecutar_site_survey.bat # Script de ejecución
├── 📄 iniciar_servidor.py     # Servidor principal
├── 📁 nuevo_baseado/          # Aplicación Python
│   ├── 📄 app.py              # Aplicación Flask
│   ├── 📄 run_app.py          # Ejecutor
│   ├── 📁 templates/          # Plantillas HTML
│   ├── 📁 static/             # Archivos estáticos
│   └── 📁 uploads/            # Archivos subidos
├── 📁 img/                    # Imágenes
└── 📄 requirements.txt        # Dependencias Python
```

## 🛠️ **Solución de Problemas**

### **Error: "Python no se reconoce"**
```bash
# Agregar Python al PATH manualmente
# Buscar: Variables de entorno del sistema
# Agregar: C:\Users\[Usuario]\AppData\Local\Programs\Python\Python3x\
```

### **Error: "Módulo no encontrado"**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **Error: "Puerto 5000 en uso"**
```bash
# Cambiar puerto en app.py
app.run(debug=False, host="127.0.0.1", port=5001)
```

### **Error: "Permisos de archivo"**
- Ejecutar como administrador
- Verificar permisos de carpeta

## 📞 **Soporte Técnico**

### **Contacto:**
- **Desarrollador:** [Tu nombre]
- **Email:** [Tu email]
- **WhatsApp:** [Tu número]

### **Horarios de Soporte:**
- **Lunes a Viernes:** 9:00 AM - 6:00 PM
- **Sábados:** 10:00 AM - 2:00 PM

### **Canales de Comunicación:**
1. **WhatsApp:** Para urgencias
2. **Email:** Para documentación
3. **Teams/Zoom:** Para reuniones técnicas

## 🔄 **Actualizaciones**

### **Proceso de Actualización:**
1. Recibir notificación de nueva versión
2. Descargar archivos actualizados
3. Hacer backup de datos actuales
4. Reemplazar archivos
5. Reiniciar aplicación
6. Verificar funcionamiento

### **Backup Automático:**
- Configurar backup diario de datos
- Guardar en Google Drive/Dropbox
- Mantener 7 días de respaldo

## 📊 **Monitoreo**

### **Verificar Estado:**
- Aplicación funcionando: ✅
- Base de datos conectada: ✅
- Archivos accesibles: ✅
- API Keys válidas: ✅

### **Logs de Error:**
- Revisar consola del navegador
- Verificar logs de Python
- Documentar errores encontrados

---

## 🎯 **Checklist de Implementación**

- [ ] Python instalado y configurado
- [ ] Dependencias instaladas
- [ ] Archivos del proyecto copiados
- [ ] Configuración de API Keys
- [ ] Aplicación ejecutándose
- [ ] Acceso local funcionando
- [ ] Pruebas básicas realizadas
- [ ] Equipo capacitado
- [ ] Documentación entregada
- [ ] Soporte configurado

**¡Listo para usar! 🚀** 