# 🚀 Guía para el Equipo en Guadalajara

## 📋 **Bienvenidos al Proyecto Fangio Telecom**

Esta guía te ayudará a configurar y usar el sistema desde Guadalajara.

## 🎯 **Paso 1: Configuración Inicial**

### **1.1 Instalar Git**
```bash
# Descargar desde: https://git-scm.com/download/win
# O usar winget:
winget install Git.Git
```

### **1.2 Instalar Python**
```bash
# Descargar desde: https://www.python.org/downloads/
# IMPORTANTE: Marcar "Add Python to PATH"
```

### **1.3 Configurar Git**
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@fangio.com"
```

## 🎯 **Paso 2: Obtener el Proyecto**

### **2.1 Clonar desde GitHub**
```bash
# Recibirás una invitación por email
# Haz clic en "Accept invitation"

# Luego clona el repositorio
git clone https://github.com/[USUARIO]/fangio-telecom-project.git
cd fangio-telecom-project
```

### **2.2 Instalar dependencias**
```bash
# Instalar dependencias de Python
pip install -r requirements.txt
```

## 🎯 **Paso 3: Ejecutar la Aplicación**

### **3.1 Método Fácil (Recomendado)**
```bash
# Doble clic en el archivo:
instalar_proyecto.bat
```

### **3.2 Método Manual**
```bash
# Navegar a la carpeta de la aplicación
cd nuevo_baseado

# Ejecutar la aplicación
python run_app.py
```

### **3.3 Verificar que funciona**
- Abrir navegador
- Ir a: `http://127.0.0.1:5000`
- Deberías ver la aplicación funcionando

## 🎯 **Paso 4: Flujo de Trabajo Diario**

### **4.1 Antes de empezar a trabajar**
```bash
# Actualizar desde GitHub
git pull origin main

# Verificar que todo funciona
python nuevo_baseado/run_app.py
```

### **4.2 Durante el trabajo**
```bash
# Ver cambios
git status

# Ver diferencias
git diff

# Agregar cambios
git add .

# Hacer commit
git commit -m "📝 Descripción de lo que hiciste"

# Subir cambios
git push origin main
```

### **4.3 Al terminar el día**
```bash
# Hacer backup
backup_automatico.bat

# Subir cambios finales
git add .
git commit -m "🏁 Cambios del día"
git push origin main
```

## 🎯 **Paso 5: Comunicación con CDMX**

### **5.1 Reportar problemas**
1. Ve a GitHub: https://github.com/[USUARIO]/fangio-telecom-project
2. Haz clic en "Issues"
3. Haz clic en "New Issue"
4. Selecciona "Bug report"
5. Completa el formulario
6. Haz clic en "Submit new issue"

### **5.2 Solicitar nuevas funcionalidades**
1. Ve a "Issues"
2. Haz clic en "New Issue"
3. Selecciona "Feature request"
4. Describe lo que necesitas
5. Asigna prioridad
6. Envía la solicitud

### **5.3 Comunicación directa**
- **WhatsApp:** Para urgencias
- **Email:** Para documentación
- **Teams/Zoom:** Para reuniones

## 🎯 **Paso 6: Solución de Problemas**

### **6.1 Error: "Python no se reconoce"**
```bash
# Verificar instalación
python --version

# Si no funciona, agregar al PATH:
# Buscar: Variables de entorno del sistema
# Agregar: C:\Users\[Usuario]\AppData\Local\Programs\Python\Python3x\
```

### **6.2 Error: "Módulo no encontrado"**
```bash
# Reinstalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

### **6.3 Error: "Puerto 5000 en uso"**
```bash
# Cambiar puerto en app.py
# Buscar: app.run(debug=False, host="127.0.0.1", port=5000)
# Cambiar a: app.run(debug=False, host="127.0.0.1", port=5001)
```

### **6.4 Error: "Git no se reconoce"**
```bash
# Reinstalar Git
# Descargar desde: https://git-scm.com/download/win
# Marcar "Add to PATH" durante instalación
```

## 🎯 **Paso 7: Funcionalidades Principales**

### **7.1 Gestión de Enlaces PtP**
- Abrir: `ptpFangio.html`
- Funciones:
  - Agregar enlaces
  - Ver perfil de elevación
  - Exportar datos
  - Análisis de enlaces

### **7.2 Gestión de Enlaces PtMP**
- Abrir: `ptmpFangio.html`
- Funciones:
  - Configurar estación base
  - Gestionar clientes
  - Análisis de cobertura

### **7.3 Aplicación Python**
- Acceder: `http://127.0.0.1:5000`
- Funciones:
  - Site Survey
  - Generación de reportes
  - Análisis de datos

## 🎯 **Paso 8: Backups y Seguridad**

### **8.1 Backup automático**
```bash
# Ejecutar backup manual
backup_automatico.bat

# El backup se guarda en: backup_[FECHA]_[HORA].zip
```

### **8.2 Backup manual**
```bash
# Copiar carpeta completa
# Guardar en Google Drive/Dropbox
# Nombrar: Fangio_Backup_[FECHA]
```

### **8.3 Seguridad**
- No compartir credenciales
- No subir archivos sensibles a GitHub
- Hacer backup antes de cambios grandes

## 🎯 **Paso 9: Actualizaciones**

### **9.1 Recibir actualizaciones**
```bash
# Actualizar desde GitHub
git pull origin main

# Verificar cambios
git log --oneline -5
```

### **9.2 Instalar nueva versión**
```bash
# Descargar desde GitHub Releases
# O usar git pull si ya tienes el repositorio

# Hacer backup antes
backup_automatico.bat

# Reemplazar archivos
# Reiniciar aplicación
```

## 🎯 **Paso 10: Monitoreo**

### **10.1 Verificar estado**
- [ ] Aplicación funcionando
- [ ] Base de datos conectada
- [ ] Archivos accesibles
- [ ] Backup reciente

### **10.2 Logs de error**
- Revisar consola del navegador (F12)
- Verificar logs de Python
- Documentar errores encontrados

## 📞 **Contacto y Soporte**

### **Horarios de Soporte:**
- **Lunes a Viernes:** 9:00 AM - 6:00 PM
- **Sábados:** 10:00 AM - 2:00 PM

### **Canales de Comunicación:**
1. **GitHub Issues:** Para problemas técnicos
2. **WhatsApp:** Para urgencias
3. **Email:** Para documentación
4. **Teams/Zoom:** Para reuniones

### **Contacto CDMX:**
- **Desarrollador:** [Nombre]
- **Email:** [email]
- **WhatsApp:** [número]

## ✅ **Checklist de Configuración**

- [ ] Git instalado y configurado
- [ ] Python instalado y configurado
- [ ] Repositorio clonado
- [ ] Dependencias instaladas
- [ ] Aplicación ejecutándose
- [ ] Acceso local funcionando
- [ ] Pruebas básicas realizadas
- [ ] Backup configurado
- [ ] Comunicación establecida
- [ ] Documentación leída

---

## 🚀 **¡Listo para Trabajar!**

Una vez completado este checklist, estarás listo para trabajar en el proyecto Fangio Telecom desde Guadalajara.

**Recuerda:**
- Siempre hacer backup antes de cambios grandes
- Comunicar problemas a través de GitHub Issues
- Mantener el código actualizado con `git pull`
- Documentar cambios importantes

**¡Bienvenido al equipo! 🎉** 