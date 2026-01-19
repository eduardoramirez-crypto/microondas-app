#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Caché y Optimización de Base de Datos para Fangio Telecom
Optimiza consultas y reduce latencia
"""

import os
import json
import time
import hashlib
import logging
from functools import lru_cache, wraps
from typing import Dict, List, Any, Optional, Union
import redis
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from datetime import datetime, timedelta

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fangio_cache.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RedisCache:
    """Sistema de caché con Redis"""
    
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
            # Verificar conexión
            self.redis_client.ping()
            self.connected = True
            logger.info("✅ Conexión a Redis establecida")
        except Exception as e:
            logger.warning(f"⚠️ No se pudo conectar a Redis: {e}")
            self.connected = False
            self.redis_client = None
    
    def get(self, key: str, default=None):
        """Obtiene un valor del caché"""
        if not self.connected:
            return default
        
        try:
            value = self.redis_client.get(key)
            if value is not None:
                return json.loads(value)
            return default
        except Exception as e:
            logger.error(f"❌ Error obteniendo clave {key}: {e}")
            return default
    
    def set(self, key: str, value: Any, timeout: int = 3600):
        """Establece un valor en el caché"""
        if not self.connected:
            return False
        
        try:
            serialized_value = json.dumps(value, default=str)
            return self.redis_client.setex(key, timeout, serialized_value)
        except Exception as e:
            logger.error(f"❌ Error estableciendo clave {key}: {e}")
            return False
    
    def delete(self, key: str):
        """Elimina una clave del caché"""
        if not self.connected:
            return False
        
        try:
            return self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"❌ Error eliminando clave {key}: {e}")
            return False
    
    def exists(self, key: str):
        """Verifica si existe una clave"""
        if not self.connected:
            return False
        
        try:
            return self.redis_client.exists(key)
        except Exception as e:
            logger.error(f"❌ Error verificando clave {key}: {e}")
            return False
    
    def clear_pattern(self, pattern: str):
        """Limpia claves que coincidan con un patrón"""
        if not self.connected:
            return False
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"❌ Error limpiando patrón {pattern}: {e}")
            return False

class DatabaseOptimizer:
    """Optimizador de base de datos con caché inteligente"""
    
    def __init__(self, cache: RedisCache):
        self.cache = cache
        self.query_cache = {}
        self.connection_pool = {}
        self.stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'db_queries': 0,
            'total_time': 0
        }
    
    def cached_query(self, timeout: int = 3600, key_prefix: str = ""):
        """Decorador para cachear consultas de base de datos"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generar clave de caché
                cache_key = self._generate_cache_key(func, args, kwargs, key_prefix)
                
                # Intentar obtener del caché
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    self.stats['cache_hits'] += 1
                    logger.info(f"📋 Cache hit para {cache_key}")
                    return cached_result
                
                # Si no está en caché, ejecutar consulta
                self.stats['cache_misses'] += 1
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    
                    # Guardar en caché
                    self.cache.set(cache_key, result, timeout)
                    
                    # Actualizar estadísticas
                    query_time = time.time() - start_time
                    self.stats['db_queries'] += 1
                    self.stats['total_time'] += query_time
                    
                    logger.info(f"💾 Consulta cacheada: {cache_key} en {query_time:.2f}s")
                    return result
                    
                except Exception as e:
                    logger.error(f"❌ Error en consulta cacheada: {e}")
                    raise
            
            return wrapper
        return decorator
    
    def _generate_cache_key(self, func, args, kwargs, prefix: str):
        """Genera una clave única para el caché"""
        # Crear hash de la función y argumentos
        key_data = {
            'function': func.__name__,
            'args': args,
            'kwargs': kwargs,
            'prefix': prefix
        }
        
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return f"fangio:db:{prefix}:{hashlib.md5(key_string.encode()).hexdigest()}"
    
    def batch_query(self, queries: List[Dict], max_workers: int = 4):
        """Ejecuta múltiples consultas en paralelo"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_query = {
                executor.submit(self._execute_single_query, query): query
                for query in queries
            }
            
            for future in as_completed(future_to_query):
                query = future_to_query[future]
                try:
                    result = future.result()
                    results[query['id']] = result
                except Exception as e:
                    logger.error(f"❌ Error en consulta por lotes: {e}")
                    results[query['id']] = {'error': str(e)}
        
        return results
    
    def _execute_single_query(self, query: Dict):
        """Ejecuta una consulta individual"""
        try:
            # Aquí iría la lógica real de consulta a la base de datos
            # Por ahora simulamos una consulta
            time.sleep(0.1)  # Simular latencia
            
            return {
                'success': True,
                'data': query.get('data', {}),
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"❌ Error ejecutando consulta: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_stats(self):
        """Obtiene estadísticas de rendimiento"""
        avg_time = (self.stats['total_time'] / self.stats['db_queries'] 
                   if self.stats['db_queries'] > 0 else 0)
        
        cache_hit_rate = (self.stats['cache_hits'] / 
                         (self.stats['cache_hits'] + self.stats['cache_misses']) * 100
                         if (self.stats['cache_hits'] + self.stats['cache_misses']) > 0 else 0)
        
        return {
            'cache_hits': self.stats['cache_hits'],
            'cache_misses': self.stats['cache_misses'],
            'db_queries': self.stats['db_queries'],
            'total_time': self.stats['total_time'],
            'average_query_time': avg_time,
            'cache_hit_rate': cache_hit_rate
        }

class FileCache:
    """Sistema de caché para archivos"""
    
    def __init__(self, cache: RedisCache, base_path: str = "uploads"):
        self.cache = cache
        self.base_path = base_path
        self.file_metadata = {}
        self.compression_cache = {}
    
    def cache_file_metadata(self, file_path: str, metadata: Dict):
        """Cachea metadatos de un archivo"""
        try:
            file_hash = self._get_file_hash(file_path)
            cache_key = f"fangio:file:metadata:{file_hash}"
            
            # Agregar timestamp
            metadata['cached_at'] = time.time()
            metadata['file_path'] = file_path
            
            self.cache.set(cache_key, metadata, timeout=86400)  # 24 horas
            self.file_metadata[file_path] = metadata
            
            logger.info(f"💾 Metadatos cacheados para {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error cacheando metadatos: {e}")
            return False
    
    def get_file_metadata(self, file_path: str):
        """Obtiene metadatos de un archivo del caché"""
        try:
            file_hash = self._get_file_hash(file_path)
            cache_key = f"fangio:file:metadata:{file_hash}"
            
            # Intentar obtener del caché
            cached_metadata = self.cache.get(cache_key)
            if cached_metadata:
                logger.info(f"📋 Metadatos obtenidos de caché para {file_path}")
                return cached_metadata
            
            # Si no está en caché, generar metadatos
            metadata = self._generate_file_metadata(file_path)
            if metadata:
                self.cache_file_metadata(file_path, metadata)
            
            return metadata
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo metadatos: {e}")
            return None
    
    def _generate_file_metadata(self, file_path: str):
        """Genera metadatos para un archivo"""
        try:
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            file_size = stat.st_size
            modified_time = stat.st_mtime
            
            # Determinar tipo de archivo
            file_extension = os.path.splitext(file_path)[1].lower()
            
            metadata = {
                'file_name': os.path.basename(file_path),
                'file_size': file_size,
                'file_extension': file_extension,
                'modified_time': modified_time,
                'created_time': stat.st_ctime,
                'is_image': file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
                'is_document': file_extension in ['.pdf', '.doc', '.docx', '.xls', '.xlsx'],
                'is_map': file_extension in ['.kmz', '.kml']
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"❌ Error generando metadatos: {e}")
            return None
    
    def _get_file_hash(self, file_path: str):
        """Genera hash único para un archivo"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"❌ Error generando hash: {e}")
            return hashlib.md5(file_path.encode()).hexdigest()
    
    def clear_file_cache(self, file_path: str = None):
        """Limpia caché de archivos"""
        try:
            if file_path:
                # Limpiar caché específico
                file_hash = self._get_file_hash(file_path)
                cache_key = f"fangio:file:metadata:{file_hash}"
                self.cache.delete(cache_key)
                
                if file_path in self.file_metadata:
                    del self.file_metadata[file_path]
                
                logger.info(f"🧹 Caché limpiado para {file_path}")
            else:
                # Limpiar todo el caché de archivos
                self.cache.clear_pattern("fangio:file:*")
                self.file_metadata.clear()
                logger.info("🧹 Caché de archivos completamente limpiado")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error limpiando caché: {e}")
            return False

class QueryOptimizer:
    """Optimizador de consultas SQL/Google Sheets"""
    
    def __init__(self, cache: RedisCache):
        self.cache = cache
        self.query_plans = {}
        self.index_suggestions = {}
    
    def optimize_query(self, query: str, params: Dict = None):
        """Optimiza una consulta antes de ejecutarla"""
        try:
            # Generar plan de consulta
            query_plan = self._generate_query_plan(query, params)
            
            # Verificar si ya tenemos un plan optimizado
            plan_hash = hashlib.md5(query.encode()).hexdigest()
            if plan_hash in self.query_plans:
                optimized_query = self.query_plans[plan_hash]
                logger.info(f"📋 Plan de consulta optimizado encontrado en caché")
            else:
                # Optimizar consulta
                optimized_query = self._apply_optimizations(query, query_plan)
                self.query_plans[plan_hash] = optimized_query
            
            return optimized_query
            
        except Exception as e:
            logger.error(f"❌ Error optimizando consulta: {e}")
            return query
    
    def _generate_query_plan(self, query: str, params: Dict = None):
        """Genera un plan de consulta"""
        # En producción, aquí se analizaría la consulta real
        # Por ahora simulamos un plan básico
        return {
            'query_type': 'SELECT',
            'tables': ['enlaces'],
            'estimated_rows': 1000,
            'complexity': 'LOW'
        }
    
    def _apply_optimizations(self, query: str, plan: Dict):
        """Aplica optimizaciones a la consulta"""
        optimized_query = query
        
        # Agregar LIMIT si no existe
        if 'LIMIT' not in query.upper() and plan['estimated_rows'] > 100:
            optimized_query += " LIMIT 100"
        
        # Agregar ORDER BY si no existe
        if 'ORDER BY' not in query.upper():
            optimized_query += " ORDER BY id"
        
        return optimized_query
    
    def suggest_indexes(self, table_name: str, query_patterns: List[str]):
        """Sugiere índices para optimizar consultas"""
        try:
            suggestions = []
            
            for pattern in query_patterns:
                if 'WHERE' in pattern.upper():
                    # Sugerir índices para cláusulas WHERE
                    if 'id =' in pattern.lower():
                        suggestions.append(f"CREATE INDEX idx_{table_name}_id ON {table_name}(id)")
                    
                    if 'nombre' in pattern.lower():
                        suggestions.append(f"CREATE INDEX idx_{table_name}_nombre ON {table_name}(nombre)")
                    
                    if 'latitud' in pattern.lower() and 'longitud' in pattern.lower():
                        suggestions.append(f"CREATE INDEX idx_{table_name}_coords ON {table_name}(latitud, longitud)")
            
            self.index_suggestions[table_name] = suggestions
            return suggestions
            
        except Exception as e:
            logger.error(f"❌ Error sugiriendo índices: {e}")
            return []

class PerformanceMonitor:
    """Monitor de rendimiento del sistema"""
    
    def __init__(self):
        self.metrics = {
            'response_times': [],
            'memory_usage': [],
            'cpu_usage': [],
            'cache_performance': [],
            'database_performance': []
        }
        self.start_time = time.time()
        self.lock = threading.Lock()
    
    def record_metric(self, metric_type: str, value: float, metadata: Dict = None):
        """Registra una métrica de rendimiento"""
        try:
            with self.lock:
                if metric_type in self.metrics:
                    metric_data = {
                        'value': value,
                        'timestamp': time.time(),
                        'metadata': metadata or {}
                    }
                    self.metrics[metric_type].append(metric_data)
                    
                    # Mantener solo las últimas 1000 métricas
                    if len(self.metrics[metric_type]) > 1000:
                        self.metrics[metric_type] = self.metrics[metric_type][-1000:]
                    
                    logger.debug(f"📊 Métrica registrada: {metric_type} = {value}")
            
        except Exception as e:
            logger.error(f"❌ Error registrando métrica: {e}")
    
    def get_performance_summary(self):
        """Obtiene un resumen del rendimiento"""
        try:
            summary = {
                'uptime': time.time() - self.start_time,
                'total_metrics': sum(len(metrics) for metrics in self.metrics.values()),
                'average_response_time': 0,
                'cache_hit_rate': 0,
                'database_query_time': 0
            }
            
            # Calcular métricas promedio
            if self.metrics['response_times']:
                response_times = [m['value'] for m in self.metrics['response_times']]
                summary['average_response_time'] = sum(response_times) / len(response_times)
            
            if self.metrics['cache_performance']:
                cache_metrics = [m['value'] for m in self.metrics['cache_performance']]
                summary['cache_hit_rate'] = sum(cache_metrics) / len(cache_metrics)
            
            if self.metrics['database_performance']:
                db_metrics = [m['value'] for m in self.metrics['database_performance']]
                summary['database_query_time'] = sum(db_metrics) / len(db_metrics)
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Error generando resumen: {e}")
            return {}
    
    def export_metrics(self, file_path: str = None):
        """Exporta métricas a un archivo"""
        try:
            if file_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_path = f"fangio_metrics_{timestamp}.json"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, indent=2, default=str)
            
            logger.info(f"📁 Métricas exportadas a {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"❌ Error exportando métricas: {e}")
            return None

# Función para crear instancia global del sistema de caché
def create_cache_system():
    """Crea y configura el sistema de caché completo"""
    try:
        # Crear instancia de Redis
        cache = RedisCache()
        
        # Crear optimizadores
        db_optimizer = DatabaseOptimizer(cache)
        file_cache = FileCache(cache)
        query_optimizer = QueryOptimizer(cache)
        performance_monitor = PerformanceMonitor()
        
        logger.info("✅ Sistema de caché y optimización creado exitosamente")
        
        return {
            'cache': cache,
            'db_optimizer': db_optimizer,
            'file_cache': file_cache,
            'query_optimizer': query_optimizer,
            'performance_monitor': performance_monitor
        }
        
    except Exception as e:
        logger.error(f"❌ Error creando sistema de caché: {e}")
        return None

# Función para limpiar todo el sistema de caché
def cleanup_cache_system(cache_system):
    """Limpia todo el sistema de caché"""
    try:
        if cache_system and cache_system['cache']:
            # Limpiar caché de Redis
            cache_system['cache'].clear_pattern("fangio:*")
            
            # Limpiar cachés locales
            if 'file_cache' in cache_system:
                cache_system['file_cache'].clear_file_cache()
            
            if 'db_optimizer' in cache_system:
                cache_system['db_optimizer'].query_cache.clear()
            
            logger.info("🧹 Sistema de caché completamente limpiado")
            return True
            
    except Exception as e:
        logger.error(f"❌ Error limpiando sistema de caché: {e}")
        return False

if __name__ == "__main__":
    # Crear y probar el sistema de caché
    logger.info("🚀 Iniciando sistema de caché y optimización")
    
    cache_system = create_cache_system()
    if cache_system:
        # Probar funcionalidades
        cache = cache_system['cache']
        
        # Probar caché básico
        test_data = {'test': 'data', 'timestamp': time.time()}
        cache.set('test_key', test_data, 60)
        retrieved_data = cache.get('test_key')
        
        if retrieved_data == test_data:
            logger.info("✅ Prueba de caché básico exitosa")
        else:
            logger.error("❌ Prueba de caché básico falló")
        
        # Limpiar sistema
        cleanup_cache_system(cache_system)
    else:
        logger.error("❌ No se pudo crear el sistema de caché") 