# 🚀 Diseño de Solución - Llenado Automático

## Descripción

Esta funcionalidad permite generar automáticamente documentos de **Diseño de Solución** utilizando la plantilla `llenadoauto.xlsx` y llenando automáticamente todos los campos desde la base de datos de Google Sheets.

## 🔧 Características

- **Llenado automático completo** desde la base de datos
- **Plantilla específica** para diseño de solución (`llenadoauto.xlsx`)
- **Validación de hojas** requeridas
- **Manejo de errores** robusto
- **Logs detallados** para depuración

## 📋 Requisitos

### 1. Plantilla Excel
- **Archivo:** `llenadoauto.xlsx`
- **Ubicación:** `Temp/plantillas/llenadoauto.xlsx`
- **Formato:** Archivo Excel válido (.xlsx)

### 2. Hojas Requeridas
La plantilla debe contener las siguientes hojas:
- `0. Carátula`
- `1. Información General A`
- `2. Información General B`
- `3. Espacios en Torre y Piso A-B`
- `4. Planos A`
- `5. Planos B`
- `6. Reporte Fotos A`
- `7. Reporte Fotos B`

### 3. Base de Datos
- **Fuente:** Google Sheets (configurada en `GOOGLE_SHEETS_CSV_URL`)
- **Campos requeridos:** Ver sección de campos mapeados

## 🎯 Cómo Usar

### Opción 1: Formulario Web
1. Accede a `/test_diseno_solucion`
2. Ingresa el ID del sitio
3. Selecciona "Diseño de Solución"
4. Haz clic en "Generar Diseño de Solución"

### Opción 2: API Directa
```bash
POST /procesar
Content-Type: multipart/form-data

user_id: 5140066159E
tipo: diseno_solucion
fila_idx: (opcional)
```

### Opción 3: Desde el Sistema Principal
1. Ve a la función de diseño de solución
2. Selecciona el tipo "diseno_solucion"
3. El sistema automáticamente usará la plantilla correcta

## 📊 Campos Mapeados

### Información General A
| Campo de BD | Celda Excel | Descripción |
|-------------|-------------|-------------|
| `NOMBRE DEL SITIO` | `J9` | Nombre del sitio principal |
| `PROPIETARIO` | `M10` | Propietario del sitio |
| `ID` | `AF9` | ID del sitio |
| `ESTADO` | `AC15` | Estado donde se ubica |
| `Calle` | `D14` | Dirección de la calle |
| `Colonia` | `D15` | Colonia o barrio |
| `Municipio` | `E16` | Municipio o ciudad |
| `C.P` | `AC14` | Código postal |
| `Referencias` | `J17` | Referencias de ubicación |
| `Nombre de contacto en sitio` | `H19` | Contacto principal |
| `Telefono` | `AB19` | Teléfono de contacto |
| `LATITUD (TORRE)` | `K30` | Latitud de la torre |
| `LONGITUD (TORRE)` | `AA30` | Longitud de la torre |
| `LATITUD (FACHADA)` | `K27` | Latitud de la fachada |
| `LONGITUD (FACHADA)` | `AA27` | Longitud de la fachada |
| `Altitud (msnm)` | `M31` | Altitud sobre el nivel del mar |

### Información General B
| Campo de BD | Celda Excel | Descripción |
|-------------|-------------|-------------|
| `Nombre del sitio 2` | `J9` | Nombre del sitio secundario |
| `PROPIETARIO 2` | `M10` | Propietario del sitio 2 |
| `ID 2` | `AF9` | ID del sitio 2 |
| `ESTADO 2` | `AC15` | Estado del sitio 2 |
| `Calle 2` | `D14` | Dirección del sitio 2 |
| `Colonia 2` | `D15` | Colonia del sitio 2 |
| `Municipio 2` | `E16` | Municipio del sitio 2 |
| `C.P 2` | `AC14` | Código postal del sitio 2 |
| `Referencias 2` | `J17` | Referencias del sitio 2 |
| `Nombre de contacto en sitio 2` | `H19` | Contacto del sitio 2 |
| `Telefono 2` | `AB19` | Teléfono del sitio 2 |
| `LATITUD (TORRE) 2` | `K30` | Latitud torre sitio 2 |
| `LONGITUD (TORRE) 2` | `AA30` | Longitud torre sitio 2 |
| `LATITUD (FACHADA) 2` | `K27` | Latitud fachada sitio 2 |
| `LONGITUD (FACHADA) 2` | `AA27` | Longitud fachada sitio 2 |
| `Altitud (msnm) 2` | `M31` | Altitud sitio 2 |

### Checkboxes Automáticos

#### Tipo de Zona
- **Urbana:** `L21`
- **Suburbana:** `P21`
- **Rural:** `U21`
- **Ejidal:** `X21`
- **Pueblo Mágico:** `AB21`

#### Visibilidad del Sitio
- **Sí:** `P22`
- **No:** `S22`

#### Tipo de Camino
- **Terracería:** `G23`
- **Pavimentado:** `L23`
- **Empedrado:** `Q23`
- **Mixto:** `V23`

#### Tipo de Torre
- **Autosoportada:** `H34`
- **Arriostrada:** `P34`
- **Monopolo:** `W34`
- **Minipolo:** `AC34`
- **Otro:** `AH34`

### Campos de Espacios en Torre
| Campo de BD | Celda Excel | Descripción |
|-------------|-------------|-------------|
| `Altura de la Torre` | `L36` | Altura total de la torre |
| `Altura Edificio1` | `AF36` | Altura del edificio |
| `Nivel inferior de franja disponible` | `U37` | Nivel inferior disponible |
| `Nivel superior de franja disponible` | `AI37` | Nivel superior disponible |
| `Altura de MW conforme a topologia` | `C40` | Altura MW según topología |
| `Azimut RB` | `N40` | Azimut del radio base |
| `Propuesta de altura de antena de MW1` | `AC40` | Altura propuesta antena MW |
| `Propuesta de altura de antena de MW (SD)1` | `AH40` | Altura propuesta antena MW SD |

## 🚀 Flujo de Procesamiento

1. **Recepción de solicitud** con tipo `diseno_solucion`
2. **Validación de plantilla** `llenadoauto.xlsx`
3. **Verificación de hojas** requeridas
4. **Lectura de datos** desde Google Sheets
5. **Llenado automático** de todos los campos
6. **Generación del archivo** final
7. **Descarga automática** del documento

## 🔍 Depuración

### Logs del Sistema
El sistema genera logs detallados con el prefijo `🔧 DEBUG:`:
```
🔧 DEBUG: Procesando DISEÑO DE SOLUCIÓN
🔧 DEBUG: Hojas disponibles en plantilla de diseño: ['0. Carátula', '1. Información General A', ...]
🔧 DEBUG: Iniciando llenado automático para diseño de solución...
🔧 DEBUG: Carátula llenada: Sitio A - Sitio B
🔧 DEBUG: Campo 'NOMBRE DEL SITIO' -> Celda J9 = 'Valor'
```

### Errores Comunes
- **Plantilla no encontrada:** Verificar ruta `Temp/plantillas/llenadoauto.xlsx`
- **Hojas faltantes:** Verificar que la plantilla tenga todas las hojas requeridas
- **Error de Excel:** Cerrar Excel y cualquier programa que use el archivo
- **Permisos:** Verificar permisos de lectura/escritura en la carpeta

## 📁 Estructura de Archivos

```
nuevo_baseado/
├── app.py                          # Aplicación principal con lógica de diseño
├── test_diseno_solucion.html      # Página de prueba
├── README_DISENO_SOLUCION.md      # Este archivo
└── Temp/
    └── plantillas/
        └── llenadoauto.xlsx       # Plantilla de diseño de solución
```

## 🎉 Beneficios

- **Ahorro de tiempo:** Llenado automático en segundos
- **Precisión:** Sin errores de transcripción manual
- **Consistencia:** Formato uniforme en todos los documentos
- **Escalabilidad:** Procesa múltiples sitios rápidamente
- **Auditoría:** Logs completos de todo el proceso

## 🔧 Personalización

### Agregar Nuevos Campos
1. Agregar el campo en el diccionario correspondiente
2. Verificar que la celda existe en la plantilla
3. Probar con datos de ejemplo

### Modificar Mapeo de Celdas
1. Editar los diccionarios de mapeo
2. Actualizar la documentación
3. Verificar que las nuevas celdas existen

### Agregar Nuevas Hojas
1. Agregar la hoja a `required_sheets_diseno`
2. Obtener referencia con `wb_diseno.sheets['Nombre Hoja']`
3. Implementar llenado específico para la nueva hoja

## 📞 Soporte

Para problemas o preguntas sobre esta funcionalidad:
1. Revisar los logs del sistema
2. Verificar la estructura de la plantilla
3. Confirmar que los campos de la BD existen
4. Revisar permisos de archivos y carpetas

---

**Desarrollado por FANGIO TELECOM** 🚀
