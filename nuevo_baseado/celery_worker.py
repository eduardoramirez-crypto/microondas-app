#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Worker de Celery para Fangio Telecom
Procesamiento asíncrono de archivos y optimizaciones
"""

import os
import time
import json
import logging
from celery import Celery
from PIL import Image
import io
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import redis
from functools import lru_cache
import hashlib
import xlwings as xw
from werkzeug.utils import secure_filename

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fangio_celery.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuración de Celery
CELERY_CONFIG = {
    'broker_url': 'redis://localhost:6379/0',
    'result_backend': 'redis://localhost:6379/0',
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
    'timezone': 'America/Mexico_City',
    'enable_utc': True,
    'task_track_started': True,
    'task_time_limit': 30 * 60,  # 30 minutos
    'task_soft_time_limit': 25 * 60,  # 25 minutos
    'worker_prefetch_multiplier': 1,
    'worker_max_tasks_per_child': 1000,
    'worker_disable_rate_limits': False,
    'worker_max_memory_per_child': 200000,  # 200MB
}

# Crear instancia de Celery
celery_app = Celery('fangio_worker')
celery_app.config_from_object(CELERY_CONFIG)

# Configuración de Redis
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

# Configuración de directorios
UPLOAD_FOLDER = 'uploads'
TEMP_FOLDER = 'temp'
PROCESSED_FOLDER = 'processed'

# Crear directorios si no existen
for folder in [UPLOAD_FOLDER, TEMP_FOLDER, PROCESSED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

class ImageProcessor:
    """Procesador optimizado de imágenes"""
    
    def __init__(self, quality=85, max_size=(1920, 1080)):
        self.quality = quality
        self.max_size = max_size
        self.supported_formats = ['JPEG', 'PNG', 'WEBP']
    
    def compress_image(self, image_path, output_path=None):
        """Comprime y optimiza una imagen"""
        try:
            start_time = time.time()
            
            with Image.open(image_path) as img:
                # Convertir a RGB si es necesario
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionar si es muy grande
                if img.size[0] > self.max_size[0] or img.size[1] > self.max_size[1]:
                    img.thumbnail(self.max_size, Image.Resampling.LANCZOS)
                
                # Determinar formato de salida
                if output_path is None:
                    output_path = image_path
                
                # Comprimir y guardar
                img.save(
                    output_path,
                    format='JPEG',
                    quality=self.quality,
                    optimize=True,
                    progressive=True
                )
            
            processing_time = time.time() - start_time
            logger.info(f"✅ Imagen comprimida: {image_path} en {processing_time:.2f}s")
            
            return {
                'success': True,
                'original_size': os.path.getsize(image_path),
                'compressed_size': os.path.getsize(output_path),
                'compression_ratio': round(
                    (1 - os.path.getsize(output_path) / os.path.getsize(image_path)) * 100, 2
                ),
                'processing_time': processing_time
            }
            
        except Exception as e:
            logger.error(f"❌ Error comprimiendo imagen {image_path}: {e}")
            return {'success': False, 'error': str(e)}
    
    def batch_compress(self, image_paths, max_workers=4):
        """Comprime múltiples imágenes en paralelo"""
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_path = {
                executor.submit(self.compress_image, path): path 
                for path in image_paths
            }
            
            for future in as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    result = future.result()
                    results.append((path, result))
                except Exception as e:
                    logger.error(f"❌ Error en compresión por lotes para {path}: {e}")
                    results.append((path, {'success': False, 'error': str(e)}))
        
        return results

class FileProcessor:
    """Procesador optimizado de archivos"""
    
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.cache = {}
    
    def process_file(self, file_path, file_type):
        """Procesa un archivo según su tipo"""
        try:
            start_time = time.time()
            
            if file_type.startswith('image/'):
                result = self.image_processor.compress_image(file_path)
            elif file_type == 'application/pdf':
                result = self.validate_pdf(file_path)
            elif file_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                result = self.validate_excel(file_path)
            else:
                result = {'success': True, 'message': 'Archivo no requiere procesamiento'}
            
            processing_time = time.time() - start_time
            result['processing_time'] = processing_time
            
            # Cachear resultado
            file_hash = self.get_file_hash(file_path)
            self.cache[file_hash] = result
            
            logger.info(f"✅ Archivo procesado: {file_path} en {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error procesando archivo {file_path}: {e}")
            return {'success': False, 'error': str(e)}
    
    def validate_pdf(self, file_path):
        """Valida un archivo PDF"""
        try:
            # Verificar que el archivo sea un PDF válido
            with open(file_path, 'rb') as f:
                header = f.read(4)
                if header != b'%PDF':
                    return {'success': False, 'error': 'Archivo no es un PDF válido'}
            
            file_size = os.path.getsize(file_path)
            return {
                'success': True,
                'file_size': file_size,
                'is_valid_pdf': True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def validate_excel(self, file_path):
        """Valida un archivo Excel"""
        try:
            # Verificar que el archivo sea un Excel válido
            df = pd.read_excel(file_path, nrows=1)
            file_size = os.path.getsize(file_path)
            
            return {
                'success': True,
                'file_size': file_size,
                'columns': list(df.columns),
                'is_valid_excel': True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_file_hash(self, file_path):
        """Genera hash único para un archivo"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def batch_process(self, files_info, max_workers=4):
        """Procesa múltiples archivos en paralelo"""
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(self.process_file, info['path'], info['type']): info
                for info in files_info
            }
            
            for future in as_completed(future_to_file):
                file_info = future_to_file[future]
                try:
                    result = future.result()
                    results.append((file_info['path'], result))
                except Exception as e:
                    logger.error(f"❌ Error en procesamiento por lotes para {file_info['path']}: {e}")
                    results.append((file_info['path'], {'success': False, 'error': str(e)}))
        
        return results

class DatabaseOptimizer:
    """Optimizador de base de datos"""
    
    def __init__(self):
        self.cache_timeout = 3600  # 1 hora
    
    @lru_cache(maxsize=128)
    def get_enlace_data(self, enlace_id):
        """Obtiene datos de enlace con caché"""
        cache_key = f"enlace:{enlace_id}"
        
        # Verificar caché
        cached_data = redis_client.get(cache_key)
        if cached_data:
            logger.info(f"📋 Datos obtenidos de caché para enlace {enlace_id}")
            return json.loads(cached_data)
        
        # Si no está en caché, simular consulta a base de datos
        # En producción, aquí iría la consulta real
        data = self.query_database(enlace_id)
        
        # Guardar en caché
        redis_client.setex(cache_key, self.cache_timeout, json.dumps(data))
        logger.info(f"💾 Datos guardados en caché para enlace {enlace_id}")
        
        return data
    
    def query_database(self, enlace_id):
        """Simula consulta a base de datos"""
        # En producción, aquí iría la consulta real a Google Sheets o base de datos
        time.sleep(0.1)  # Simular latencia de red
        
        return {
            'id': enlace_id,
            'sitio_a': f'Sitio A - {enlace_id}',
            'sitio_b': f'Sitio B - {enlace_id}',
            'latitud_a': 19.4326,
            'longitud_a': -99.1332,
            'latitud_b': 20.6597,
            'longitud_b': -103.3496,
            'timestamp': time.time()
        }
    
    def batch_query(self, enlace_ids, max_workers=4):
        """Consulta múltiples enlaces en paralelo"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_id = {
                executor.submit(self.get_enlace_data, enlace_id): enlace_id
                for enlace_id in enlace_ids
            }
            
            for future in as_completed(future_to_id):
                enlace_id = future_to_id[future]
                try:
                    data = future.result()
                    results[enlace_id] = data
                except Exception as e:
                    logger.error(f"❌ Error consultando enlace {enlace_id}: {e}")
                    results[enlace_id] = {'error': str(e)}
        
        return results

# Tareas de Celery
@celery_app.task(bind=True, name='fangio.process_files')
def process_files_task(self, files_info):
    """Tarea para procesar archivos"""
    try:
        logger.info(f"🚀 Iniciando procesamiento de {len(files_info)} archivos")
        
        processor = FileProcessor()
        results = processor.batch_process(files_info)
        
        # Actualizar progreso
        self.update_state(
            state='SUCCESS',
            meta={'processed': len(results), 'total': len(files_info)}
        )
        
        logger.info(f"✅ Procesamiento completado: {len(results)} archivos")
        return {
            'success': True,
            'processed_files': len(results),
            'results': results
        }
        
    except Exception as e:
        logger.error(f"❌ Error en tarea de procesamiento: {e}")
        self.update_state(
            state='FAILURE',
            meta={'error': str(e)}
        )
        raise

@celery_app.task(bind=True, name='fangio.compress_images')
def compress_images_task(self, image_paths):
    """Tarea para comprimir imágenes"""
    try:
        logger.info(f"🖼️ Iniciando compresión de {len(image_paths)} imágenes")
        
        processor = ImageProcessor()
        results = processor.batch_compress(image_paths)
        
        # Actualizar progreso
        self.update_state(
            state='SUCCESS',
            meta={'compressed': len(results), 'total': len(image_paths)}
        )
        
        logger.info(f"✅ Compresión completada: {len(results)} imágenes")
        return {
            'success': True,
            'compressed_images': len(results),
            'results': results
        }
        
    except Exception as e:
        logger.error(f"❌ Error en tarea de compresión: {e}")
        self.update_state(
            state='FAILURE',
            meta={'error': str(e)}
        )
        raise

@celery_app.task(bind=True, name='fangio.process_enlace')
def process_enlace_task(self, enlace_id, files_data):
    """Tarea para procesar un enlace completo"""
    try:
        logger.info(f"🔗 Iniciando procesamiento del enlace {enlace_id}")
        
        # Obtener datos del enlace
        db_optimizer = DatabaseOptimizer()
        enlace_data = db_optimizer.get_enlace_data(enlace_id)
        
        # Procesar archivos
        file_processor = FileProcessor()
        files_info = [
            {'path': file_path, 'type': file_type}
            for file_path, file_type in files_data.items()
        ]
        
        file_results = file_processor.batch_process(files_info)
        
        # Generar plantilla
        template_result = generate_template(enlace_data, file_results)
        
        # Actualizar progreso
        self.update_state(
            state='SUCCESS',
            meta={'enlace_id': enlace_id, 'files_processed': len(file_results)}
        )
        
        logger.info(f"✅ Enlace {enlace_id} procesado completamente")
        return {
            'success': True,
            'enlace_id': enlace_id,
            'enlace_data': enlace_data,
            'files_processed': len(file_results),
            'template_generated': template_result
        }
        
    except Exception as e:
        logger.error(f"❌ Error procesando enlace {enlace_id}: {e}")
        self.update_state(
            state='FAILURE',
            meta={'error': str(e)}
        )
        raise

def generate_template(enlace_data, file_results):
    """Genera plantilla con datos del enlace"""
    try:
        # En producción, aquí se generaría la plantilla real
        template = {
            'enlace_id': enlace_data['id'],
            'sitio_a': enlace_data['sitio_a'],
            'sitio_b': enlace_data['sitio_b'],
            'files_processed': len(file_results),
            'timestamp': time.time()
        }
        
        return template
        
    except Exception as e:
        logger.error(f"❌ Error generando plantilla: {e}")
        return None

# Función para monitorear el estado de las tareas
def get_task_status(task_id):
    """Obtiene el estado de una tarea"""
    try:
        task = celery_app.AsyncResult(task_id)
        return {
            'task_id': task_id,
            'status': task.status,
            'result': task.result if task.ready() else None,
            'info': task.info
        }
    except Exception as e:
        logger.error(f"❌ Error obteniendo estado de tarea {task_id}: {e}")
        return {'error': str(e)}

# Función para limpiar tareas completadas
def cleanup_completed_tasks():
    """Limpia tareas completadas del broker"""
    try:
        # Limpiar resultados de tareas completadas
        celery_app.control.purge()
        logger.info("🧹 Tareas completadas limpiadas")
        return True
    except Exception as e:
        logger.error(f"❌ Error limpiando tareas: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Iniciando worker de Celery para Fangio Telecom")
    
    # Configurar worker
    celery_app.conf.update(
        worker_concurrency=4,
        worker_prefetch_multiplier=1,
        task_acks_late=True,
        worker_disable_rate_limits=False
    )
    
    # Iniciar worker
    celery_app.worker_main(['worker', '--loglevel=info', '--concurrency=4']) 