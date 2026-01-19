# FANGIO TELECOM - Sistema Multi-Usuario

## 🚀 Características del Sistema Robusto

### ✅ Gestión de Usuarios Concurrentes
- **Máximo 10 usuarios simultáneos**
- **Timeout de sesión**: 30 minutos de inactividad
- **Gestión automática de sesiones**
- **Limpieza automática de usuarios inactivos**

### 🔧 Gestión de Procesos Excel
- **Cierre automático de procesos Excel**
- **Prevención de bloqueos de archivos**
- **Limpieza forzada de procesos huérfanos**
- **Gestión por usuario individual**

### 📁 Limpieza Automática
- **Archivos temporales**: Eliminación automática después de 1 hora
- **Procesos Excel**: Cierre automático al terminar operaciones
- **Sesiones inactivas**: Limpieza automática

## 📋 Formas de Iniciar la Aplicación

### Opción 1: Script Robusto (Recomendado)
```bash
# Doble clic en:
iniciar_app_robusto.bat
```

### Opción 2: Script con Ngrok (Acceso Remoto)
```bash
# Doble clic en:
iniciar_con_ngrok.bat
```

### Opción 3: Manual
```bash
cd nuevo_baseado
pip install -r requirements.txt
python app.py
```

## 🌐 URLs Disponibles

### Local
- **Página principal**: `http://127.0.0.1:5000`
- **PTP Fangio**: `http://127.0.0.1:5000/ptpFangio`
- **Login**: `http://127.0.0.1:5000/login.html`

### Remoto (con ngrok)
- **Página principal**: `https://[URL-NGROK]/`
- **PTP Fangio**: `https://[URL-NGROK]/ptpFangio`
- **Login**: `https://[URL-NGROK]/login.html`

## 🛠️ Rutas de Administración

### Estado del Sistema
```
GET /estado_sistema
```
Muestra:
- Número de usuarios activos
- Máximo de usuarios permitidos
- Lista de usuarios activos
- Número de procesos Excel

### Limpieza Manual
```
GET /limpiar_archivos_temp
```
Limpia archivos temporales

```
GET /limpiar_archivos_temp_forzado
```
Limpia archivos temporales y fuerza cierre de Excel

## 🔍 Monitoreo del Sistema

### Ver Estado en Tiempo Real
```bash
curl http://127.0.0.1:5000/estado_sistema
```

### Limpiar Procesos Excel
```bash
curl http://127.0.0.1:5000/limpiar_archivos_temp_forzado
```

## ⚠️ Solución de Problemas

### Error: "Sistema ocupado"
- **Causa**: Máximo de usuarios alcanzado
- **Solución**: Esperar a que usuarios inactivos se desconecten automáticamente

### Error: "Archivo en uso"
- **Causa**: Proceso Excel no se cerró correctamente
- **Solución**: Usar `/limpiar_archivos_temp_forzado`

### Error: "No se puede conectar"
- **Causa**: Aplicación Flask no está corriendo
- **Solución**: Verificar que `python app.py` esté ejecutándose

## 📊 Logs del Sistema

La aplicación muestra logs detallados:
- 🔍 Procesos Excel encontrados
- ✅ Procesos terminados correctamente
- ⚠️ Errores de limpieza
- 🗑️ Archivos temporales eliminados

## 🔒 Seguridad

- **Sesiones únicas**: Cada usuario tiene un ID único
- **Timeout automático**: Sesiones expiran después de 30 minutos
- **Limpieza de procesos**: No quedan procesos Excel huérfanos
- **Gestión de memoria**: Archivos temporales se eliminan automáticamente

## 📞 Soporte

Si tienes problemas:
1. Verifica el estado del sistema: `/estado_sistema`
2. Limpia procesos forzadamente: `/limpiar_archivos_temp_forzado`
3. Reinicia la aplicación con el script robusto 