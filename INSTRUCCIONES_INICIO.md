# 🚀 FANGIO TELECOM - Instrucciones de Inicio

## ✅ Métodos para Iniciar la Aplicación

### 📋 Opción 1: Archivo Batch (RECOMENDADO)
**Para usuarios de Windows:**
1. Haz doble clic en `INICIAR_APP.bat`
2. La aplicación se iniciará automáticamente
3. El navegador se abrirá en `http://127.0.0.1:5000`

### 🐍 Opción 2: Script Python
**Para usuarios avanzados:**
```bash
python iniciar_app.py
```

### ⚡ Opción 3: Comando Manual
**Para desarrolladores:**
```bash
cd nuevo_baseado
python app.py
```

## 🎯 Características del Sistema de Inicio

### ✅ Verificaciones Automáticas
- ✅ Verifica que existe el directorio `nuevo_baseado`
- ✅ Verifica que existe el archivo `app.py`
- ✅ Cambia automáticamente al directorio correcto
- ✅ Abre el navegador automáticamente

### 🛡️ Manejo de Errores
- ❌ Si falta `nuevo_baseado`: Muestra error claro
- ❌ Si falta `app.py`: Muestra error claro
- ❌ Si hay problemas de Python: Muestra detalles del error

### 🌐 Funcionalidades
- 🚀 Inicia la aplicación Flask
- 🌐 Abre automáticamente el navegador
- 📍 URL: `http://127.0.0.1:5000`
- 🛑 Para detener: `Ctrl+C`

## 📁 Estructura de Archivos

```
mejorar/
├── INICIAR_APP.bat          ← Archivo principal para iniciar
├── iniciar_app.py           ← Script Python alternativo
├── INSTRUCCIONES_INICIO.md  ← Este archivo
└── nuevo_baseado/
    ├── app.py               ← Aplicación Flask
    ├── templates/
    │   └── index.html       ← Página principal
    └── static/              ← Archivos estáticos
```

## 🔧 Solución de Problemas

### ❌ Error: "No se encontró el directorio 'nuevo_baseado'"
**Solución:** Asegúrate de ejecutar el archivo desde el directorio raíz del proyecto.

### ❌ Error: "No se encontró el archivo 'app.py'"
**Solución:** Verifica que el archivo `app.py` esté en `nuevo_baseado/app.py`.

### ❌ Error: "Template not found"
**Solución:** La aplicación debe ejecutarse desde `nuevo_baseado/`, no desde el directorio raíz.

### ❌ Error: "Module not found"
**Solución:** Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🎉 ¡Listo!

Una vez que la aplicación esté corriendo, podrás:
- 📊 Acceder a la base de datos de enlaces
- 🔍 Buscar registros por ID
- 📝 Generar documentos automáticamente
- 📈 Crear reportes y análisis

---

**Desarrollado por:** Efren Alexis Hernandez Mendez  
**Empresa:** FANGIO TELECOM  
**Año:** 2025 