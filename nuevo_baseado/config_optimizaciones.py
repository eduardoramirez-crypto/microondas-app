# Configuración de Optimizaciones para Fangio Telecom
# Archivo de configuración para máximo rendimiento

import os
from datetime import timedelta

# Configuración de caché Redis
REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': None,
    'decode_responses': True
}

# Configuración de compresión de imágenes
IMAGE_COMPRESSION = {
    'quality': 85,
    'max_width': 1920,
    'max_height': 1080,
    'formats': ['JPEG', 'PNG', 'WEBP'],
    'enable_webp': True
}

# Configuración de procesamiento en lotes
BATCH_PROCESSING = {
    'max_workers': 4,
    'chunk_size': 10,
    'timeout': 30
}

# Configuración de caché
CACHE_CONFIG = {
    'default_timeout': 3600,  # 1 hora
    'key_prefix': 'fangio:',
    'max_entries': 1000
}

# Configuración de archivos
FILE_CONFIG = {
    'max_size': 100 * 1024 * 1024,  # 100MB
    'allowed_extensions': {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
        'documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx'],
        'maps': ['.kmz', '.kml']
    },
    'upload_folder': 'uploads',
    'temp_folder': 'temp'
}

# Configuración de CDN
CDN_CONFIG = {
    'enabled': True,
    'domain': 'cdn.fangio.com.mx',
    'https': True,
    'cache_control': 'public, max-age=31536000'  # 1 año
}

# Configuración de base de datos
DB_CONFIG = {
    'connection_pool_size': 10,
    'query_timeout': 30,
    'enable_query_cache': True,
    'batch_size': 100
}

# Configuración de logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'fangio_optimized.log',
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Configuración de performance
PERFORMANCE_CONFIG = {
    'enable_gzip': True,
    'enable_brotli': True,
    'enable_minification': True,
    'enable_concatenation': True,
    'enable_tree_shaking': True
}

# Configuración de workers
WORKER_CONFIG = {
    'celery_workers': 4,
    'thread_pool_size': 8,
    'process_pool_size': 4,
    'max_concurrent_tasks': 100
}

# Configuración de monitoreo
MONITORING_CONFIG = {
    'enable_metrics': True,
    'enable_profiling': True,
    'enable_health_checks': True,
    'metrics_interval': 60  # segundos
}

# Configuración de seguridad
SECURITY_CONFIG = {
    'rate_limit': {
        'requests': 100,
        'window': 60  # segundos
    },
    'file_validation': True,
    'virus_scan': True,
    'encryption': True
}

# Configuración de backup
BACKUP_CONFIG = {
    'auto_backup': True,
    'backup_interval': 24,  # horas
    'backup_retention': 7,  # días
    'compression': True
}

# Configuración de notificaciones
NOTIFICATION_CONFIG = {
    'email_notifications': True,
    'sms_notifications': False,
    'push_notifications': True,
    'webhook_notifications': True
}

# Configuración de desarrollo
DEV_CONFIG = {
    'debug_mode': False,
    'hot_reload': False,
    'profiling': True,
    'logging_level': 'DEBUG'
}

# Función para obtener configuración según el entorno
def get_config(environment='production'):
    """Retorna la configuración según el entorno"""
    if environment == 'development':
        return {
            **globals(),
            'DEV_CONFIG': {**DEV_CONFIG, 'debug_mode': True, 'hot_reload': True}
        }
    elif environment == 'testing':
        return {
            **globals(),
            'DB_CONFIG': {**DB_CONFIG, 'connection_pool_size': 5},
            'WORKER_CONFIG': {**WORKER_CONFIG, 'celery_workers': 2}
        }
    else:  # production
        return globals()

# Función para validar configuración
def validate_config(config):
    """Valida que la configuración sea correcta"""
    required_keys = ['REDIS_CONFIG', 'FILE_CONFIG', 'DB_CONFIG']
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Configuración requerida faltante: {key}")
    
    return True

# Función para aplicar configuración
def apply_config(config):
    """Aplica la configuración al sistema"""
    try:
        validate_config(config)
        
        # Aplicar configuraciones del sistema
        os.environ['FANGIO_MAX_FILE_SIZE'] = str(config['FILE_CONFIG']['max_size'])
        os.environ['FANGIO_CACHE_TIMEOUT'] = str(config['CACHE_CONFIG']['default_timeout'])
        os.environ['FANGIO_WORKER_COUNT'] = str(config['WORKER_CONFIG']['celery_workers'])
        
        print("✅ Configuración aplicada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error aplicando configuración: {e}")
        return False

if __name__ == "__main__":
    # Aplicar configuración por defecto
    config = get_config()
    apply_config(config) 