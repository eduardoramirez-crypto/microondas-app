#!/usr/bin/env python3
"""
Configuración para la funcionalidad de Diseño de Solución
FANGIO TELECOM
"""

import os

# ===== CONFIGURACIÓN DE PLANTILLA =====
PLANTILLA_DISENO_SOLUCION = "llenadoauto.xlsx"
RUTA_PLANTILLA = os.path.join("Temp", "plantillas", PLANTILLA_DISENO_SOLUCION)

# ===== HOJAS REQUERIDAS =====
HOJAS_REQUERIDAS = [
    '0. Carátula',
    '1. Información General A',
    '2. Información General B',
    '3. Espacios en Torre y Piso A-B',
    '4. Planos A',
    '5. Planos B',
    '6. Reporte Fotos A',
    '7. Reporte Fotos B'
]

# ===== MAPEO DE CAMPOS - INFORMACIÓN GENERAL A =====
CAMPOS_A_CELDAS = {
    'NOMBRE DEL SITIO': 'J9',
    'PROPIETARIO': 'M10',
    'ID': 'AF9',
    'ESTADO ': 'AC15',
    'Calle': 'D14',
    'Colonia': 'D15',
    'Municipio': 'E16',
    'C.P': 'AC14',
    'Referencias': 'J17',
    'Nombre de contacto en sitio': 'H19',
    'Telefono': 'AB19',
    'LATITUD (TORRE)': 'K30',
    'LONGITUD (TORRE)': 'AA30',
    'LATITUD (FACHADA)': 'K27',
    'LONGITUD (FACHADA)': 'AA27',
    'Altitud (msnm)': 'M31'
}

# ===== MAPEO DE CAMPOS - INFORMACIÓN GENERAL B =====
CAMPOS_B_CELDAS = {
    'Nombre del sitio 2': 'J9',
    'PROPIETARIO 2': 'M10',
    'ID 2': 'AF9',
    'ESTADO 2': 'AC15',
    'Calle 2': 'D14',
    'Colonia 2': 'D15',
    'Municipio 2': 'E16',
    'C.P 2': 'AC14',
    'Referencias 2': 'J17',
    'Nombre de contacto en sitio 2': 'H19',
    'Telefono 2': 'AB19',
    'LATITUD (TORRE) 2': 'K30',
    'LONGITUD (TORRE) 2': 'AA30',
    'LATITUD (FACHADA) 2': 'K27',
    'LONGITUD (FACHADA) 2': 'AA27',
    'Altitud (msnm) 2': 'M31'
}

# ===== MAPEO DE CHECKBOXES - TIPO DE ZONA =====
CHECKBOXES_TIPO_ZONA = {
    'urbana': 'L21',
    'suburbana': 'P21',
    'rural': 'U21',
    'ejidal': 'X21',
    'pueblo mágico': 'AB21'
}

# ===== MAPEO DE CHECKBOXES - VISIBILIDAD =====
CHECKBOXES_VISIBILIDAD = {
    'si': 'P22',
    'no': 'S22'
}

# ===== MAPEO DE CHECKBOXES - TIPO DE CAMINO =====
CHECKBOXES_TIPO_CAMINO = {
    'terracería': 'G23',
    'pavimentado': 'L23',
    'empedrado': 'Q23',
    'mixto': 'V23'
}

# ===== MAPEO DE CHECKBOXES - TIPO DE TORRE =====
CHECKBOXES_TIPO_TORRE = {
    'autosoportada': 'H34',
    'arriostrada': 'P34',
    'monopolo': 'W34',
    'minipolo': 'AC34',
    'otro': 'AH34'
}

# ===== MAPEO DE CAMPOS - ESPACIOS EN TORRE =====
CAMPOS_ESPACIOS_TORRE = {
    'Altura de la Torre': 'L36',
    'Altura Edificio1': 'AF36',
    'Nivel inferior de franja disponible': 'U37',
    'Nivel superior de franja disponible': 'AI37',
    'Altura de MW conforme a topologia': 'C40',
    'Azimut RB ': 'N40',
    'Propuesta de altura de antena de MW1': 'AC40',
    'Propuesta de altura de antena de MW (SD)1': 'AH40'
}

# ===== CONFIGURACIÓN DE SALIDA =====
PREFIJO_ARCHIVO_SALIDA = "DISENO_SOLUCION_"
EXTENSION_ARCHIVO = ".xlsx"

# ===== CONFIGURACIÓN DE LOGS =====
PREFIJO_LOG = "🔧 DEBUG:"
PREFIJO_ADVERTENCIA = "⚠️ ADVERTENCIA:"

# ===== CONFIGURACIÓN DE EXCEL =====
EXCEL_VISIBLE = False
MAX_INTENTOS_APERTURA = 3
TIEMPO_ESPERA_ENTRE_INTENTOS = 2  # segundos

# ===== VALIDACIÓN DE ARCHIVO =====
SIGNATURA_EXCEL = b'PK\x03\x04'  # Signatura de archivo .xlsx
TAMANO_MINIMO_PLANTILLA = 1000  # bytes

# ===== FUNCIONES DE UTILIDAD =====
def obtener_ruta_plantilla():
    """Retorna la ruta completa de la plantilla"""
    return RUTA_PLANTILLA

def obtener_nombre_archivo_salida(user_id):
    """Genera el nombre del archivo de salida"""
    return f"{PREFIJO_ARCHIVO_SALIDA}{user_id}{EXTENSION_ARCHIVO}"

def validar_plantilla(ruta_plantilla):
    """Valida que la plantilla sea un archivo Excel válido"""
    try:
        if not os.path.exists(ruta_plantilla):
            return False, f"Plantilla no encontrada: {ruta_plantilla}"
        
        with open(ruta_plantilla, 'rb') as f:
            signature = f.read(4)
            if signature != SIGNATURA_EXCEL:
                return False, "Archivo no es un Excel válido (.xlsx)"
        
        file_size = os.path.getsize(ruta_plantilla)
        if file_size < TAMANO_MINIMO_PLANTILLA:
            return False, f"Archivo muy pequeño ({file_size} bytes), puede estar corrupto"
        
        return True, "Plantilla válida"
        
    except Exception as e:
        return False, f"Error al validar plantilla: {e}"

def obtener_configuracion_completa():
    """Retorna toda la configuración en un diccionario"""
    return {
        'plantilla': {
            'nombre': PLANTILLA_DISENO_SOLUCION,
            'ruta': RUTA_PLANTILLA,
            'hojas_requeridas': HOJAS_REQUERIDAS
        },
        'mapeo_campos': {
            'informacion_a': CAMPOS_A_CELDAS,
            'informacion_b': CAMPOS_B_CELDAS,
            'espacios_torre': CAMPOS_ESPACIOS_TORRE
        },
        'mapeo_checkboxes': {
            'tipo_zona': CHECKBOXES_TIPO_ZONA,
            'visibilidad': CHECKBOXES_VISIBILIDAD,
            'tipo_camino': CHECKBOXES_TIPO_CAMINO,
            'tipo_torre': CHECKBOXES_TIPO_TORRE
        },
        'configuracion': {
            'excel_visible': EXCEL_VISIBLE,
            'max_intentos': MAX_INTENTOS_APERTURA,
            'tiempo_espera': TIEMPO_ESPERA_ENTRE_INTENTOS,
            'prefijo_log': PREFIJO_LOG,
            'prefijo_advertencia': PREFIJO_ADVERTENCIA
        }
    }

# ===== FUNCIÓN DE PRUEBA =====
if __name__ == "__main__":
    print("🔧 CONFIGURACIÓN DE DISEÑO DE SOLUCIÓN")
    print("=" * 40)
    
    # Mostrar configuración
    config = obtener_configuracion_completa()
    
    print(f"📁 Plantilla: {config['plantilla']['nombre']}")
    print(f"📍 Ruta: {config['plantilla']['ruta']}")
    print(f"📋 Hojas requeridas: {len(config['plantilla']['hojas_requeridas'])}")
    
    # Validar plantilla
    es_valida, mensaje = validar_plantilla(RUTA_PLANTILLA)
    print(f"✅ Validación: {'Válida' if es_valida else 'Inválida'}")
    if not es_valida:
        print(f"   ❌ {mensaje}")
    
    # Mostrar mapeos
    print(f"\n📊 Mapeo de campos:")
    print(f"   - Información A: {len(config['mapeo_campos']['informacion_a'])} campos")
    print(f"   - Información B: {len(config['mapeo_campos']['informacion_b'])} campos")
    print(f"   - Espacios torre: {len(config['mapeo_campos']['espacios_torre'])} campos")
    
    print(f"\n🔘 Mapeo de checkboxes:")
    print(f"   - Tipo zona: {len(config['mapeo_checkboxes']['tipo_zona'])} opciones")
    print(f"   - Visibilidad: {len(config['mapeo_checkboxes']['visibilidad'])} opciones")
    print(f"   - Tipo camino: {len(config['mapeo_checkboxes']['tipo_camino'])} opciones")
    print(f"   - Tipo torre: {len(config['mapeo_checkboxes']['tipo_torre'])} opciones")
    
    print(f"\n⚙️ Configuración:")
    print(f"   - Excel visible: {config['configuracion']['excel_visible']}")
    print(f"   - Max intentos: {config['configuracion']['max_intentos']}")
    print(f"   - Tiempo espera: {config['configuracion']['tiempo_espera']}s")
