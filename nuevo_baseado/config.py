#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración centralizada para FANGIO TELECOM
Archivo de configuración del sistema
"""

import os
from typing import Dict, Any, Optional

class Config:
    """Configuración base de la aplicación"""
    
    # Configuración básica
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fangio-telecom-secret-key-2025'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # URLs de Google Sheets
    GOOGLE_SHEETS_CSV_URL = os.environ.get('GOOGLE_SHEETS_CSV_URL') or \
        'https://docs.google.com/spreadsheets/d/1sfOY1Y3dNVCOT8zyCMzpgARv-R_jRE-S/export?format=csv'
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE_PREFIX = 'fangio_app'
    
    # Configuración de archivos
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {
        'images': {'.jpg', '.jpeg', '.png', '.gif', '.bmp'},
        'documents': {'.pdf', '.doc', '.docx', '.xls', '.xlsx'},
        'archives': {'.zip', '.rar', '.7z'},
        'kmz': {'.kmz', '.kml'}
    }
    
    # Directorios del sistema
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'Temp', 'plantillas')
    SITE_SURVEY_DIR = os.path.join(BASE_DIR, 'site_survey')
    PTMP_SURVEY_DIR = os.path.join(BASE_DIR, 'ptmp_site_survey')
    GENERATED_FILES_DIR = os.path.join(BASE_DIR, 'archivos_generados')
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    
    # Configuración de Excel
    EXCEL_TEMPLATES = {
        'site_survey': 'EJEMPLO SS VACIO.xlsx',
        'ptmp_survey': 'EJEMPLO SS PtMP VACIO.xlsx',
        'diseno_solucion': 'llenadoauto.xlsx'
    }
    
    # Configuración de seguridad
    MAX_LOGIN_ATTEMPTS = 3
    SESSION_TIMEOUT = 3600  # 1 hora en segundos
    
    # Configuración de rendimiento
    MAX_WORKERS = int(os.environ.get('MAX_WORKERS', '4'))
    CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', '300'))  # 5 minutos
    
    # Configuración de monitoreo
    ENABLE_METRICS = os.environ.get('ENABLE_METRICS', 'True').lower() == 'true'
    METRICS_INTERVAL = int(os.environ.get('METRICS_INTERVAL', '60'))  # segundos

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    ENABLE_METRICS = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    ENABLE_METRICS = True
    
    # Configuraciones de producción
    MAX_WORKERS = int(os.environ.get('MAX_WORKERS', '8'))
    CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', '600'))  # 10 minutos

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    
    # Directorios de prueba
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOADS_DIR = os.path.join(BASE_DIR, 'test_uploads')
    GENERATED_FILES_DIR = os.path.join(BASE_DIR, 'test_generated')
    LOGS_DIR = os.path.join(BASE_DIR, 'test_logs')

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: Optional[str] = None) -> Config:
    """
    Obtiene la configuración según el entorno
    
    Args:
        config_name: Nombre de la configuración ('development', 'production', 'testing')
        
    Returns:
        Config: Objeto de configuración
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])

def create_directories():
    """Crea los directorios necesarios para el sistema"""
    config_obj = get_config()
    
    directories = [
        config_obj.UPLOADS_DIR,
        config_obj.TEMPLATES_DIR,
        config_obj.SITE_SURVEY_DIR,
        config_obj.PTMP_SURVEY_DIR,
        config_obj.GENERATED_FILES_DIR,
        config_obj.LOGS_DIR
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directorio creado/verificado: {directory}")

def validate_config():
    """Valida la configuración del sistema"""
    config_obj = get_config()
    
    print("🔍 Validando configuración del sistema...")
    
    # Verificar URLs
    if not config_obj.GOOGLE_SHEETS_CSV_URL:
        print("⚠️  GOOGLE_SHEETS_CSV_URL no está configurado")
    else:
        print("✅ GOOGLE_SHEETS_CSV_URL configurado")
    
    # Verificar directorios
    create_directories()
    
    # Verificar plantillas
    for template_type, template_name in config_obj.EXCEL_TEMPLATES.items():
        template_path = os.path.join(config_obj.TEMPLATES_DIR, template_name)
        if os.path.exists(template_path):
            print(f"✅ Plantilla {template_type}: {template_name}")
        else:
            print(f"⚠️  Plantilla {template_type} no encontrada: {template_path}")
    
    print("✅ Validación de configuración completada")

if __name__ == '__main__':
    # Ejecutar validación si se ejecuta directamente
    validate_config()
