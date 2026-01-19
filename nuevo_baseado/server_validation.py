#!/usr/bin/env python3
"""
Módulo de validación del lado del servidor para proteger operaciones críticas
Este archivo debe ejecutarse en el servidor para validar todas las operaciones importantes
"""

import hashlib
import hmac
import time
import json
import secrets
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServerValidator:
    def __init__(self, secret_key: str = None):
        """
        Inicializar el validador del servidor
        
        Args:
            secret_key: Clave secreta para firmar tokens (se genera automáticamente si no se proporciona)
        """
        self.secret_key = secret_key or secrets.token_hex(32)
        self.session_tokens = {}
        self.rate_limits = {}
        self.max_requests_per_minute = 60
        
    def generate_token(self, user_id: str, operation: str) -> str:
        """
        Generar token de autenticación para una operación específica
        
        Args:
            user_id: Identificador del usuario
            operation: Tipo de operación a realizar
            
        Returns:
            Token firmado para la operación
        """
        timestamp = int(time.time())
        payload = {
            'user_id': user_id,
            'operation': operation,
            'timestamp': timestamp,
            'nonce': secrets.token_hex(16)
        }
        
        # Crear firma HMAC
        message = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        token = {
            'payload': payload,
            'signature': signature
        }
        
        # Almacenar token en sesión
        token_id = hashlib.sha256(message.encode()).hexdigest()[:16]
        self.session_tokens[token_id] = {
            'token': token,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(minutes=30)
        }
        
        return token_id
    
    def validate_token(self, token_id: str, operation: str) -> bool:
        """
        Validar token de autenticación
        
        Args:
            token_id: ID del token a validar
            operation: Operación que se intenta realizar
            
        Returns:
            True si el token es válido, False en caso contrario
        """
        if token_id not in self.session_tokens:
            logger.warning(f"Token no encontrado: {token_id}")
            return False
        
        token_data = self.session_tokens[token_id]
        
        # Verificar expiración
        if datetime.now() > token_data['expires_at']:
            logger.warning(f"Token expirado: {token_id}")
            del self.session_tokens[token_id]
            return False
        
        token = token_data['token']
        payload = token['payload']
        
        # Verificar operación
        if payload['operation'] != operation:
            logger.warning(f"Operación no coincide: esperada {operation}, recibida {payload['operation']}")
            return False
        
        # Verificar firma
        message = json.dumps(payload, sort_keys=True)
        expected_signature = hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(token['signature'], expected_signature):
            logger.warning(f"Firma inválida para token: {token_id}")
            return False
        
        return True
    
    def check_rate_limit(self, client_ip: str) -> bool:
        """
        Verificar límite de velocidad para prevenir ataques
        
        Args:
            client_ip: Dirección IP del cliente
            
        Returns:
            True si está dentro del límite, False si excede
        """
        current_time = time.time()
        minute_window = int(current_time // 60)
        
        if client_ip not in self.rate_limits:
            self.rate_limits[client_ip] = {}
        
        if minute_window not in self.rate_limits[client_ip]:
            self.rate_limits[client_ip][minute_window] = 0
        
        # Limpiar ventanas antiguas
        for window in list(self.rate_limits[client_ip].keys()):
            if window < minute_window - 1:
                del self.rate_limits[client_ip][window]
        
        # Verificar límite
        current_requests = self.rate_limits[client_ip][minute_window]
        if current_requests >= self.max_requests_per_minute:
            logger.warning(f"Límite de velocidad excedido para IP: {client_ip}")
            return False
        
        # Incrementar contador
        self.rate_limits[client_ip][minute_window] += 1
        return True
    
    def validate_calculation_request(self, data: Dict[str, Any], client_ip: str) -> Dict[str, Any]:
        """
        Validar solicitud de cálculo de enlace PtP
        
        Args:
            data: Datos de la solicitud
            client_ip: IP del cliente
            
        Returns:
            Resultado de la validación
        """
        # Verificar límite de velocidad
        if not self.check_rate_limit(client_ip):
            return {
                'valid': False,
                'error': 'Límite de velocidad excedido. Intente nuevamente en un minuto.',
                'code': 'RATE_LIMIT_EXCEEDED'
            }
        
        # Validar campos requeridos
        required_fields = ['distancia', 'frecuencia', 'potencia_tx', 'sensibilidad_rx']
        for field in required_fields:
            if field not in data:
                return {
                    'valid': False,
                    'error': f'Campo requerido faltante: {field}',
                    'code': 'MISSING_FIELD'
                }
        
        # Validar rangos de valores
        validations = {
            'distancia': (0.1, 1000),  # km
            'frecuencia': (1, 100),    # GHz
            'potencia_tx': (-10, 50),  # dBm
            'sensibilidad_rx': (-120, -50)  # dBm
        }
        
        for field, (min_val, max_val) in validations.items():
            if field in data:
                try:
                    value = float(data[field])
                    if not (min_val <= value <= max_val):
                        return {
                            'valid': False,
                            'error': f'Valor de {field} fuera del rango permitido ({min_val}-{max_val})',
                            'code': 'INVALID_RANGE'
                        }
                except (ValueError, TypeError):
                    return {
                        'valid': False,
                        'error': f'Valor inválido para {field}',
                        'code': 'INVALID_VALUE'
                    }
        
        return {
            'valid': True,
            'message': 'Solicitud válida'
        }
    
    def validate_excel_export(self, data: Dict[str, Any], client_ip: str) -> Dict[str, Any]:
        """
        Validar solicitud de exportación a Excel
        
        Args:
            data: Datos a exportar
            client_ip: IP del cliente
            
        Returns:
            Resultado de la validación
        """
        # Verificar límite de velocidad
        if not self.check_rate_limit(client_ip):
            return {
                'valid': False,
                'error': 'Límite de velocidad excedido para exportación',
                'code': 'RATE_LIMIT_EXCEEDED'
            }
        
        # Validar que hay datos para exportar
        if not data or len(data) == 0:
            return {
                'valid': False,
                'error': 'No hay datos para exportar',
                'code': 'NO_DATA'
            }
        
        # Validar tamaño de datos (prevenir exportaciones masivas)
        data_size = len(json.dumps(data))
        max_size = 10 * 1024 * 1024  # 10MB
        
        if data_size > max_size:
            return {
                'valid': False,
                'error': 'Datos demasiado grandes para exportar',
                'code': 'DATA_TOO_LARGE'
            }
        
        return {
            'valid': True,
            'message': 'Exportación autorizada'
        }
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """
        Registrar evento de seguridad
        
        Args:
            event_type: Tipo de evento
            details: Detalles del evento
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'details': details
        }
        
        logger.info(f"Security Event: {json.dumps(log_entry)}")
        
        # Aquí podrías enviar a un sistema de monitoreo externo
        # como SIEM, Splunk, etc.

# Instancia global del validador
validator = ServerValidator()

# Funciones de conveniencia para usar en endpoints
def validate_request(request_data: Dict[str, Any], operation: str, client_ip: str) -> Dict[str, Any]:
    """
    Función de conveniencia para validar solicitudes
    
    Args:
        request_data: Datos de la solicitud
        operation: Tipo de operación
        client_ip: IP del cliente
        
    Returns:
        Resultado de la validación
    """
    if operation == 'calculation':
        return validator.validate_calculation_request(request_data, client_ip)
    elif operation == 'export':
        return validator.validate_excel_export(request_data, client_ip)
    else:
        return {
            'valid': False,
            'error': f'Operación no reconocida: {operation}',
            'code': 'UNKNOWN_OPERATION'
        }

def generate_operation_token(user_id: str, operation: str) -> str:
    """Generar token para una operación específica"""
    return validator.generate_token(user_id, operation)

def validate_operation_token(token_id: str, operation: str) -> bool:
    """Validar token de operación"""
    return validator.validate_token(token_id, operation)

if __name__ == "__main__":
    # Ejemplo de uso
    print("🛡️ Servidor de validación iniciado")
    print(f"Clave secreta: {validator.secret_key[:16]}...")
    
    # Ejemplo de generación y validación de token
    token_id = generate_operation_token("user123", "calculation")
    print(f"Token generado: {token_id}")
    
    is_valid = validate_operation_token(token_id, "calculation")
    print(f"Token válido: {is_valid}")
    
    # Ejemplo de validación de solicitud
    test_data = {
        'distancia': 5.0,
        'frecuencia': 2.4,
        'potencia_tx': 20,
        'sensibilidad_rx': -80
    }
    
    result = validate_request(test_data, 'calculation', '192.168.1.1')
    print(f"Validación de solicitud: {result}")
