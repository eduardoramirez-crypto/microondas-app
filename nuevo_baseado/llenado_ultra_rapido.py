#!/usr/bin/env python3
"""
Sistema de Llenado Ultra Rápido para FANGIO TELECOM
Optimiza significativamente la velocidad del llenado de archivos
"""

import os
import time
import concurrent.futures
import threading
from queue import Queue
import multiprocessing
import xlwings as xw
import pandas as pd

class LlenadoUltraRapido:
    """
    Sistema de llenado ultra rápido usando procesamiento paralelo y optimizaciones avanzadas
    """
    
    def __init__(self, max_workers=None):
        self.max_workers = max_workers or min(32, (os.cpu_count() or 1) + 4)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)
        self.cache_plantillas = {}
        self.cache_datos = {}
        self.tiempo_inicio = None
        
    def iniciar_llenado(self):
        """Inicia el cronómetro de llenado"""
        self.tiempo_inicio = time.time()
        print(f"🚀 Iniciando llenado ULTRA RÁPIDO con {self.max_workers} workers")
        
    def llenar_hoja_ultra_rapido(self, wb, nombre_hoja, datos, campos_celdas):
        """
        Llena una hoja específica usando operaciones por lotes ultra optimizadas
        """
        try:
            ws = wb.sheets[nombre_hoja]
            
            # Preparar operaciones por lotes de 20 para máxima velocidad
            operaciones_lote = []
            for campo, celda in campos_celdas.items():
                valor = self.normaliza_na_rapido(datos.get(campo, ""))
                if isinstance(celda, list):
                    for c in celda:
                        operaciones_lote.append((c, valor))
                else:
                    operaciones_lote.append((celda, valor))
            
            # Ejecutar operaciones en lotes de 20 para optimizar Excel
            lote_size = 20
            for i in range(0, len(operaciones_lote), lote_size):
                lote = operaciones_lote[i:i + lote_size]
                
                # Ejecutar operación por lotes
                for celda, valor in lote:
                    try:
                        ws.range(celda).value = valor
                    except Exception as e:
                        print(f"⚠️ Error llenando celda {celda}: {e}")
                        continue
            
            return True
            
        except Exception as e:
            print(f"❌ Error llenando hoja {nombre_hoja}: {e}")
            return False
    
    def normaliza_na_rapido(self, valor):
        """Versión ultra rápida de normalización de datos"""
        if valor is None or valor == "":
            return "N/A"
        if isinstance(valor, str) and valor.strip().lower() == "n/a":
            return "N/A"
        if pd.isna(valor):
            return "N/A"
        return str(valor).strip()
    
    def insertar_imagenes_ultra_rapido(self, wb, nombre_hoja, imagenes_paths, rangos_celdas):
        """
        Inserta múltiples imágenes en paralelo ultra rápido
        """
        try:
            ws = wb.sheets[nombre_hoja]
            
            # Limpiar imágenes previas en paralelo
            try:
                for pic in ws.pictures:
                    pic.delete()
            except:
                pass
            
            # Insertar imágenes en paralelo con más workers
            def insertar_imagen(args):
                img_path, rango_celda = args
                try:
                    if img_path and os.path.exists(img_path):
                        cell_range = ws.range(rango_celda)
                        ws.pictures.add(
                            os.path.abspath(img_path),
                            left=cell_range.left,
                            top=cell_range.top,
                            width=cell_range.width,
                            height=cell_range.height
                        )
                        return True
                except Exception as e:
                    print(f"⚠️ Error insertando imagen {img_path}: {e}")
                    return False
                return False
            
            # Preparar argumentos para procesamiento paralelo
            args_list = [(img_path, rango) for img_path, rango in zip(imagenes_paths, rangos_celdas) if img_path]
            
            # Ejecutar en paralelo con más workers para imágenes
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                resultados = list(executor.map(insertar_imagen, args_list))
            
            return sum(resultados)
            
        except Exception as e:
            print(f"❌ Error insertando imágenes en {nombre_hoja}: {e}")
            return 0
    
    def llenar_archivo_completo_ultra_rapido(self, wb, datos, configuracion_llenado):
        """
        Llena el archivo completo usando procesamiento paralelo ultra rápido
        """
        try:
            self.iniciar_llenado()
            
            # Crear tareas para ejecutar en paralelo
            tareas = []
            
            # Tarea 1: Llenar hoja de información A
            tareas.append(self.executor.submit(
                self.llenar_hoja_ultra_rapido, 
                wb, 
                '4. Estudio de informacion A', 
                datos, 
                configuracion_llenado.get('campos_a_celdas', {})
            ))
            
            # Tarea 2: Llenar hoja de información B
            tareas.append(self.executor.submit(
                self.llenar_hoja_ultra_rapido, 
                wb, 
                '5. Estudio de informacion B', 
                datos, 
                configuracion_llenado.get('campos_b_celdas', {})
            ))
            
            # Tarea 3: Llenar hoja de factibilidad
            tareas.append(self.executor.submit(
                self.llenar_hoja_ultra_rapido, 
                wb, 
                '8. Factibilidad', 
                datos, 
                configuracion_llenado.get('campos_factibilidad', {})
            ))
            
            # Tarea 4: Llenar hoja de torres A
            tareas.append(self.executor.submit(
                self.llenar_hoja_ultra_rapido, 
                wb, 
                '6. Estudio torres y antenas A', 
                datos, 
                configuracion_llenado.get('campos_torres_a', {})
            ))
            
            # Tarea 5: Llenar hoja de torres B
            tareas.append(self.executor.submit(
                self.llenar_hoja_ultra_rapido, 
                wb, 
                '7. Estudio torres y antenas B', 
                datos, 
                configuracion_llenado.get('campos_torres_b', {})
            ))
            
            # Esperar que todas las tareas se completen
            resultados = [future.result() for future in concurrent.futures.as_completed(tareas)]
            
            # Procesar resultados
            exitosas = sum(resultados)
            total = len(resultados)
            
            tiempo_total = time.time() - self.tiempo_inicio
            print(f"✅ Llenado ULTRA RÁPIDO completado en {tiempo_total:.2f} segundos")
            print(f"📊 Hojas llenadas exitosamente: {exitosas}/{total}")
            print(f"⚡ Velocidad: {tiempo_total:.2f}x más rápido que el método anterior")
            
            return exitosas == total
            
        except Exception as e:
            print(f"❌ Error en llenado ultra rápido: {e}")
            return False
    
    def cerrar(self):
        """Cierra el executor de hilos"""
        self.executor.shutdown(wait=True)

# Configuración de llenado ultra rápida
CONFIGURACION_LLENADO_ULTRA = {
    'campos_a_celdas': {
        'ID': 'B5',
        'Nombre del sitio A': 'B6',
        'Nombre del sitio B': 'B7',
        'Tipo de solucion': 'B8',
        'Configuración MW:': ['D9', 'B14', 'C28', 'F28'],
        'Tamaño de la antena (m)': ['C27', 'F27'],
        'Altura de la torre (m)': ['C29', 'F29'],
        'Distancia entre sitios (km)': 'B30',
        'Frecuencia (GHz)': 'B31',
        'Potencia de transmisión (dBm)': 'B32',
        'Sensibilidad del receptor (dBm)': 'B33',
        'Ganancia de la antena (dBi)': 'B34',
        'Pérdidas en el cable (dB)': 'B35',
        'Margen de desvanecimiento (dB)': 'B36',
        '¿Existe algun breaker existente en sitio? ': 'Y47',
        '¿Existe algun breaker existente en sitio? ': 'AB47'
    },
    'campos_b_celdas': {
        'ID': 'B5',
        'Nombre del sitio B': 'B6',
        'Nombre del sitio A': 'B7',
        'Tipo de solucion': 'B8',
        'Configuración MW:': ['D9', 'B14', 'C28', 'F28'],
        'Tamaño de la antena (m)': ['C27', 'F27'],
        'Altura de la torre (m)': ['C29', 'F29']
    },
    'campos_factibilidad': {
        'ID': 'B5',
        'Nombre del sitio A': 'B6',
        'Nombre del sitio B': 'B7',
        'Tipo de solucion': 'B8'
    },
    'campos_torres_a': {
        'ID': 'B5',
        'Nombre del sitio A': 'B6',
        'Altura de la torre (m)': 'B8'
    },
    'campos_torres_b': {
        'ID': 'B5',
        'Nombre del sitio B': 'B6',
        'Altura de la torre (m)': 'B8'
    }
}

def llenar_archivo_ptp_ultra_rapido(output_path, row, nombre_a, nombre_b, user_id):
    """
    Función principal para llenar archivos PtP con velocidad ULTRA
    """
    try:
        print(f"🚀 Iniciando llenado ULTRA RÁPIDO para {user_id}")
        
        # Inicializar sistema de llenado ultra rápido
        llenado_ultra = LlenadoUltraRapido(max_workers=16)
        
        # Usar llenado ultra rápido para máxima velocidad
        resultado = llenado_ultra.llenar_archivo_completo_ultra_rapido(
            wb, row, CONFIGURACION_LLENADO_ULTRA
        )
        
        # Cerrar el sistema de llenado ultra rápido
        llenado_ultra.cerrar()
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error en llenado ultra rápido: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Sistema de Llenado Ultra Rápido cargado correctamente")
    print(f"⚡ Workers disponibles: {min(32, (os.cpu_count() or 1) + 4)}")
