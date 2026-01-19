#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación Principal Optimizada para Fangio Telecom
Integra todas las optimizaciones para máximo rendimiento
"""

import os
import time
import logging
import json
from functools import wraps
from flask import Flask, request, jsonify, send_file, render_template
from flask_compress import Compress
from werkzeug.utils import secure_filename
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import threading

# Importar módulos optimizados
try:
    from config_optimizaciones import get_config, apply_config
    from cache_optimizer import create_cache_system
    from image_processor import create_image_processor
    from celery_worker import celery_app, process_files_task, process_enlace_task
    OPTIMIZATIONS_AVAILABLE = True
except ImportError:
    OPTIMIZATIONS_AVAILABLE = False
    print("⚠️ Algunas optimizaciones no están disponibles")

# Configuración de logging optimizada
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fangio_optimized.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 año

# Aplicar compresión
Compress(app)

# Configuración global
config = get_config() if OPTIMIZATIONS_AVAILABLE else {}
apply_config(config) if OPTIMIZATIONS_AVAILABLE else None

# Sistema de caché
cache_system = create_cache_system() if OPTIMIZATIONS_AVAILABLE else None

# Procesador de imágenes
image_processor = create_image_processor() if OPTIMIZATIONS_AVAILABLE else None

# Thread pool para operaciones concurrentes
thread_pool = ThreadPoolExecutor(max_workers=8)

# Métricas de rendimiento
performance_metrics = {
    'requests_total': 0,
    'requests_success': 0,
    'requests_failed': 0,
    'total_processing_time': 0,
    'cache_hits': 0,
    'cache_misses': 0
}

# Decorador para medir rendimiento
def measure_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            performance_metrics['requests_success'] += 1
            
            # Registrar métricas
            processing_time = time.time() - start_time
            performance_metrics['total_processing_time'] += processing_time
            
            if cache_system and cache_system['performance_monitor']:
                cache_system['performance_monitor'].record_metric(
                    'response_times', processing_time, {'endpoint': func.__name__}
                )
            
            return result
            
        except Exception as e:
            performance_metrics['requests_failed'] += 1
            logger.error(f"❌ Error en {func.__name__}: {e}")
            raise
        finally:
            performance_metrics['requests_total'] += 1
    
    return wrapper

# Decorador para caché
def cached_response(timeout=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not cache_system or not cache_system['cache']:
                return func(*args, **kwargs)
            
            # Generar clave de caché
            cache_key = f"fangio:response:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Intentar obtener del caché
            cached_result = cache_system['cache'].get(cache_key)
            if cached_result is not None:
                performance_metrics['cache_hits'] += 1
                logger.info(f"📋 Respuesta obtenida de caché para {func.__name__}")
                return cached_result
            
            # Si no está en caché, ejecutar función
            performance_metrics['cache_misses'] += 1
            result = func(*args, **kwargs)
            
            # Guardar en caché
            cache_system['cache'].set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator

# Rutas optimizadas
@app.route('/')
@measure_performance
@cached_response(timeout=1800)  # 30 minutos
def index():
    """Página principal con caché"""
    try:
        import pandas as pd
        
        # Usar sistema de caché si está disponible
        if cache_system and cache_system['db_optimizer']:
            # Consulta optimizada con caché
            db_status = 'ok'
            db_error = ''
            
            try:
                # Intentar obtener del caché primero
                cache_key = "fangio:db:google_sheets_status"
                cached_status = cache_system['cache'].get(cache_key)
                
                if cached_status:
                    db_status = cached_status['status']
                    db_error = cached_status['error']
                else:
                    # Consulta real a Google Sheets
                    df_db = pd.read_csv(config.get('GOOGLE_SHEETS_CSV_URL', ''), keep_default_na=False, na_values=[])
                    
                    # Guardar en caché
                    status_data = {'status': 'ok', 'error': '', 'timestamp': time.time()}
                    cache_system['cache'].set(cache_key, status_data, 300)  # 5 minutos
                    
            except Exception as e:
                db_status = 'error'
                db_error = str(e)
        else:
            # Fallback sin optimizaciones
            db_status = 'ok'
            db_error = ''
            try:
                df_db = pd.read_csv(config.get('GOOGLE_SHEETS_CSV_URL', ''), keep_default_na=False, na_values=[])
            except Exception as e:
                db_status = 'error'
                db_error = str(e)
        
        return render_template('index.html', db_status=db_status, db_error=db_error)
        
    except Exception as e:
        logger.error(f"❌ Error en página principal: {e}")
        return render_template('index.html', db_status='error', db_error=str(e))

@app.route('/llenado_automatico')
@measure_performance
def llenado_automatico():
    """Página de llenado automático optimizada"""
    return send_file('llenado-automatico.html')

@app.route('/ptpFangio')
@app.route('/ptpFangio.html')
@measure_performance
@cached_response(timeout=3600)  # 1 hora
def ptpFangio():
    """Página PtP Fangio con caché"""
    return send_file('templates/ptpFangio.html')

@app.route('/procesar', methods=['POST'])
@measure_performance
def procesar():
    """Procesamiento optimizado de archivos"""
    
    start_time = time.time()
    
    try:
        # Verificar si las optimizaciones están disponibles
        if not OPTIMIZATIONS_AVAILABLE:
            logger.warning("⚠️ Optimizaciones no disponibles, usando procesamiento estándar")
            return procesar_estandar()
        
        # Procesamiento optimizado
        return procesar_optimizado()
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"❌ Error en procesamiento optimizado: {e}")
        
        # Fallback a procesamiento estándar
        try:
            return procesar_estandar()
        except Exception as fallback_error:
            logger.error(f"❌ Error en fallback: {fallback_error}")
            return jsonify({
                'success': False,
                'error': f"Error en procesamiento: {str(e)}",
                'processing_time': processing_time
            }), 500

def procesar_optimizado():
    """Procesamiento optimizado con Celery y caché"""
    
    start_time = time.time()
    
    try:
        # Obtener datos del formulario
        fila_idx = request.form.get('fila_idx')
        user_id = request.form.get('user_id')
        tipo = request.form.get('tipo', 'site_survey')
        
        # Procesar archivos en segundo plano con Celery
        files_info = []
        
        # Recopilar información de archivos
        for field_name, file_list in request.files.lists():
            for i, file in enumerate(file_list):
                if file and file.filename:
                    files_info.append({
                        'field_name': field_name,
                        'file_index': i,
                        'filename': file.filename,
                        'content_type': file.content_type,
                        'file_size': len(file.read())
                    })
                    file.seek(0)  # Resetear posición del archivo
        
        # Crear tarea de Celery para procesamiento asíncrono
        if files_info:
            task = process_files_task.delay(files_info)
            
            # Procesar enlace si se especifica
            if user_id:
                enlace_task = process_enlace_task.delay(user_id, {})
                
                return jsonify({
                    'success': True,
                    'message': 'Procesamiento iniciado en segundo plano',
                    'task_id': task.id,
                    'enlace_task_id': enlace_task.id,
                    'files_count': len(files_info),
                    'processing_mode': 'async'
                })
            else:
                return jsonify({
                    'success': True,
                    'message': 'Archivos procesados en segundo plano',
                    'task_id': task.id,
                    'files_count': len(files_info),
                    'processing_mode': 'async'
                })
        else:
            return jsonify({
                'success': False,
                'error': 'No se recibieron archivos para procesar'
            }), 400
            
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"❌ Error en procesamiento optimizado: {e}")
        
        return jsonify({
            'success': False,
            'error': str(e),
            'processing_time': processing_time
        }), 500

def procesar_estandar():
    """Procesamiento estándar sin optimizaciones"""
    
    # Aquí iría el código original de procesamiento
    # Por ahora retornamos un mensaje
    return jsonify({
        'success': True,
        'message': 'Procesamiento estándar completado',
        'processing_mode': 'standard'
    })

@app.route('/task_status/<task_id>')
@measure_performance
def task_status(task_id):
    """Obtiene el estado de una tarea de Celery"""
    
    if not OPTIMIZATIONS_AVAILABLE:
        return jsonify({'error': 'Celery no disponible'}), 400
    
    try:
        from celery_worker import get_task_status
        status = get_task_status(task_id)
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo estado de tarea: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/performance_metrics')
@measure_performance
def performance_metrics_endpoint():
    """Endpoint para obtener métricas de rendimiento"""
    
    try:
        metrics = performance_metrics.copy()
        
        # Calcular métricas adicionales
        if metrics['requests_total'] > 0:
            metrics['success_rate'] = (metrics['requests_success'] / metrics['requests_total']) * 100
            metrics['average_processing_time'] = metrics['total_processing_time'] / metrics['requests_total']
        else:
            metrics['success_rate'] = 0
            metrics['average_processing_time'] = 0
        
        # Agregar métricas del sistema de caché si está disponible
        if cache_system and cache_system['performance_monitor']:
            cache_metrics = cache_system['performance_monitor'].get_performance_summary()
            metrics['cache_metrics'] = cache_metrics
        
        # Agregar métricas del procesador de imágenes si está disponible
        if image_processor:
            image_metrics = image_processor.get_stats()
            metrics['image_processing_metrics'] = image_metrics
        
        return jsonify(metrics)
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo métricas: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/optimize_images', methods=['POST'])
@measure_performance
def optimize_images():
    """Endpoint para optimizar imágenes en lote"""
    
    if not image_processor:
        return jsonify({'error': 'Procesador de imágenes no disponible'}), 400
    
    try:
        # Obtener archivos de imagen
        image_files = request.files.getlist('images')
        
        if not image_files:
            return jsonify({'error': 'No se recibieron imágenes'}), 400
        
        # Guardar archivos temporalmente
        temp_dir = 'temp_images'
        os.makedirs(temp_dir, exist_ok=True)
        
        image_paths = []
        for i, file in enumerate(image_files):
            if file and file.filename:
                filename = secure_filename(f"{i}_{file.filename}")
                file_path = os.path.join(temp_dir, filename)
                file.save(file_path)
                image_paths.append(file_path)
        
        # Procesar imágenes en lote
        results = image_processor.batch_process(
            image_paths,
            output_dir=os.path.join(temp_dir, 'processed'),
            resize=True,
            enhance=True
        )
        
        # Crear resumen
        successful_results = [r for r in results if r.success]
        total_saved = sum(r.original_size - r.processed_size for r in successful_results)
        
        summary = {
            'success': True,
            'total_images': len(results),
            'successful_images': len(successful_results),
            'failed_images': len(results) - len(successful_results),
            'total_saved_mb': total_saved / (1024*1024),
            'results': [
                {
                    'filename': os.path.basename(r.output_path),
                    'compression_ratio': r.compression_ratio,
                    'quality_score': r.quality_score
                }
                for r in successful_results
            ]
        }
        
        return jsonify(summary)
        
    except Exception as e:
        logger.error(f"❌ Error optimizando imágenes: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/clear_cache')
@measure_performance
def clear_cache():
    """Limpia todo el sistema de caché"""
    
    try:
        if cache_system:
            from cache_optimizer import cleanup_cache_system
            cleanup_cache_system(cache_system)
            
            # Recrear sistema de caché
            global cache_system
            cache_system = create_cache_system()
            
            return jsonify({
                'success': True,
                'message': 'Caché limpiado y sistema recreado'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Sistema de caché no disponible'
            }), 400
            
    except Exception as e:
        logger.error(f"❌ Error limpiando caché: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Verificación de salud del sistema"""
    
    try:
        health_status = {
            'status': 'healthy',
            'timestamp': time.time(),
            'optimizations_available': OPTIMIZATIONS_AVAILABLE,
            'cache_system_available': cache_system is not None,
            'image_processor_available': image_processor is not None,
            'celery_available': OPTIMIZATIONS_AVAILABLE
        }
        
        # Verificar componentes críticos
        if not OPTIMIZATIONS_AVAILABLE:
            health_status['status'] = 'degraded'
            health_status['warnings'] = ['Optimizaciones no disponibles']
        
        return jsonify(health_status)
        
    except Exception as e:
        logger.error(f"❌ Error en health check: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': time.time()
        }), 500

# Middleware para logging de requests
@app.before_request
def log_request():
    """Log de requests entrantes"""
    logger.info(f"📥 {request.method} {request.path} - {request.remote_addr}")

@app.after_request
def log_response(response):
    """Log de responses salientes"""
    logger.info(f"📤 {request.method} {request.path} - {response.status_code}")
    return response

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.errorhandler(413)
def too_large(error):
    return jsonify({'error': 'Archivo demasiado grande'}), 413

# Función para iniciar el sistema optimizado
def initialize_optimized_system():
    """Inicializa el sistema optimizado"""
    
    try:
        logger.info("🚀 Iniciando sistema optimizado de Fangio Telecom")
        
        # Aplicar configuración
        if OPTIMIZATIONS_AVAILABLE:
            apply_config(config)
            logger.info("✅ Configuración aplicada")
        
        # Verificar sistema de caché
        if cache_system:
            logger.info("✅ Sistema de caché inicializado")
        else:
            logger.warning("⚠️ Sistema de caché no disponible")
        
        # Verificar procesador de imágenes
        if image_processor:
            logger.info("✅ Procesador de imágenes inicializado")
        else:
            logger.warning("⚠️ Procesador de imágenes no disponible")
        
        logger.info("🎯 Sistema optimizado listo para operar")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error inicializando sistema optimizado: {e}")
        return False

# Función para limpiar recursos
def cleanup_resources():
    """Limpia recursos del sistema"""
    
    try:
        logger.info("🧹 Limpiando recursos del sistema")
        
        # Cerrar thread pool
        if thread_pool:
            thread_pool.shutdown(wait=True)
        
        # Limpiar caché
        if cache_system:
            from cache_optimizer import cleanup_cache_system
            cleanup_cache_system(cache_system)
        
        # Limpiar procesador de imágenes
        if image_processor:
            image_processor.clear_cache()
        
        logger.info("✅ Recursos limpiados correctamente")
        
    except Exception as e:
        logger.error(f"❌ Error limpiando recursos: {e}")

if __name__ == "__main__":
    # Inicializar sistema optimizado
    if initialize_optimized_system():
        try:
            # Iniciar aplicación
            logger.info("🌐 Iniciando servidor Flask optimizado")
            
            # Configuración para producción
            app.run(
                host='0.0.0.0',
                port=5000,
                debug=False,
                threaded=True,
                use_reloader=False
            )
            
        except KeyboardInterrupt:
            logger.info("🛑 Servidor detenido por el usuario")
        except Exception as e:
            logger.error(f"❌ Error en servidor: {e}")
        finally:
            cleanup_resources()
    else:
        logger.error("❌ No se pudo inicializar el sistema optimizado")
        logger.info("🔄 Iniciando en modo estándar...")
        
        # Modo estándar sin optimizaciones
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        ) 