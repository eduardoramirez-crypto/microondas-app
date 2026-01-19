#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de IA para Optimización Automática - Fangio Telecom
Aprendizaje automático para máxima velocidad
"""

import os
import time
import json
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass, field
from enum import Enum
import threading
import pickle
import hashlib
from datetime import datetime, timedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fangio_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OptimizationStrategy(Enum):
    """Estrategias de optimización"""
    SPEED_FIRST = 'speed_first'           # Máxima velocidad
    BALANCED = 'balanced'                  # Equilibrio velocidad/calidad
    QUALITY_FIRST = 'quality_first'        # Máxima calidad
    ADAPTIVE = 'adaptive'                  # Adaptativo según contexto
    LEARNING = 'learning'                  # Aprendizaje automático

class PerformanceMetric(Enum):
    """Métricas de rendimiento"""
    PROCESSING_TIME = 'processing_time'
    THROUGHPUT = 'throughput'
    MEMORY_USAGE = 'memory_usage'
    CPU_USAGE = 'cpu_usage'
    COMPRESSION_RATIO = 'compression_ratio'
    QUALITY_SCORE = 'quality_score'

@dataclass
class OptimizationDecision:
    """Decisión de optimización"""
    strategy: OptimizationStrategy
    parameters: Dict[str, Any]
    confidence: float
    reasoning: str
    timestamp: float
    expected_improvement: float

@dataclass
class PerformanceData:
    """Datos de rendimiento"""
    metric: PerformanceMetric
    value: float
    timestamp: float
    context: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

class AIOptimizer:
    """Optimizador basado en IA para máximo rendimiento"""
    
    def __init__(self, 
                 enable_learning: bool = True,
                 model_path: str = 'ai_models',
                 update_interval: int = 300):  # 5 minutos
        
        self.enable_learning = enable_learning
        self.model_path = model_path
        self.update_interval = update_interval
        
        # Crear directorio de modelos
        os.makedirs(model_path, exist_ok=True)
        
        # Modelos de IA
        self.models = {
            'performance_predictor': None,
            'strategy_selector': None,
            'parameter_optimizer': None
        }
        
        # Base de datos de rendimiento
        self.performance_db = []
        self.db_lock = threading.Lock()
        
        # Historial de decisiones
        self.decision_history = []
        
        # Configuración actual
        self.current_config = self._get_default_config()
        
        # Métricas de rendimiento
        self.metrics = {
            'total_optimizations': 0,
            'successful_optimizations': 0,
            'average_improvement': 0.0,
            'learning_cycles': 0
        }
        
        # Inicializar modelos
        self._initialize_models()
        
        # Iniciar aprendizaje automático
        if enable_learning:
            self._start_learning_loop()
        
        logger.info("🤖 Optimizador de IA iniciado")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Obtiene configuración por defecto"""
        return {
            'max_workers': 8,
            'chunk_size': 25,
            'compression_level': 'fast',
            'cache_size': 1000,
            'parallel_processing': True,
            'gpu_acceleration': False,
            'adaptive_quality': True
        }
    
    def _initialize_models(self):
        """Inicializa modelos de IA"""
        try:
            # Intentar cargar modelos existentes
            self._load_models()
            
            # Si no hay modelos, crear unos básicos
            if not any(self.models.values()):
                self._create_basic_models()
                
        except Exception as e:
            logger.error(f"❌ Error inicializando modelos: {e}")
            self._create_basic_models()
    
    def _load_models(self):
        """Carga modelos guardados"""
        try:
            for model_name in self.models.keys():
                model_file = os.path.join(self.model_path, f"{model_name}.pkl")
                if os.path.exists(model_file):
                    with open(model_file, 'rb') as f:
                        self.models[model_name] = pickle.load(f)
                    logger.info(f"📥 Modelo {model_name} cargado")
                    
        except Exception as e:
            logger.error(f"❌ Error cargando modelos: {e}")
    
    def _create_basic_models(self):
        """Crea modelos básicos"""
        try:
            # Modelo simple de predicción de rendimiento
            self.models['performance_predictor'] = SimplePerformancePredictor()
            
            # Selector de estrategia básico
            self.models['strategy_selector'] = BasicStrategySelector()
            
            # Optimizador de parámetros básico
            self.models['parameter_optimizer'] = BasicParameterOptimizer()
            
            logger.info("🔧 Modelos básicos creados")
            
        except Exception as e:
            logger.error(f"❌ Error creando modelos básicos: {e}")
    
    def _start_learning_loop(self):
        """Inicia bucle de aprendizaje automático"""
        def learning_worker():
            while True:
                try:
                    time.sleep(self.update_interval)
                    self._learn_from_data()
                except Exception as e:
                    logger.error(f"❌ Error en bucle de aprendizaje: {e}")
        
        thread = threading.Thread(target=learning_worker, daemon=True)
        thread.start()
        logger.info("🔄 Bucle de aprendizaje iniciado")
    
    def optimize_operation(self, 
                          operation_type: str,
                          input_data: Dict[str, Any],
                          context: Dict[str, Any] = None) -> OptimizationDecision:
        """Optimiza una operación usando IA"""
        
        start_time = time.time()
        
        try:
            # Recopilar contexto
            if context is None:
                context = self._collect_context()
            
            # Predecir rendimiento actual
            current_performance = self._predict_performance(operation_type, input_data, context)
            
            # Seleccionar estrategia óptima
            strategy = self._select_optimal_strategy(operation_type, input_data, context, current_performance)
            
            # Optimizar parámetros
            optimized_params = self._optimize_parameters(strategy, input_data, context)
            
            # Calcular mejora esperada
            expected_improvement = self._calculate_expected_improvement(
                current_performance, strategy, optimized_params
            )
            
            # Crear decisión
            decision = OptimizationDecision(
                strategy=strategy,
                parameters=optimized_params,
                confidence=self._calculate_confidence(strategy, optimized_params),
                reasoning=self._generate_reasoning(strategy, optimized_params, expected_improvement),
                timestamp=time.time(),
                expected_improvement=expected_improvement
            )
            
            # Aplicar optimización
            self._apply_optimization(decision)
            
            # Registrar decisión
            self.decision_history.append(decision)
            
            # Actualizar métricas
            self.metrics['total_optimizations'] += 1
            
            logger.info(f"🎯 Optimización aplicada: {strategy.value} - Mejora esperada: {expected_improvement:.1f}%")
            
            return decision
            
        except Exception as e:
            logger.error(f"❌ Error en optimización: {e}")
            # Retornar decisión por defecto
            return OptimizationDecision(
                strategy=OptimizationStrategy.BALANCED,
                parameters=self.current_config,
                confidence=0.5,
                reasoning=f"Error en optimización: {str(e)}",
                timestamp=time.time(),
                expected_improvement=0.0
            )
    
    def _collect_context(self) -> Dict[str, Any]:
        """Recopila contexto del sistema"""
        try:
            import psutil
            
            context = {
                'cpu_usage': psutil.cpu_percent(interval=1),
                'memory_usage': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0],
                'timestamp': time.time(),
                'active_processes': len(psutil.pids())
            }
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Error recopilando contexto: {e}")
            return {'timestamp': time.time()}
    
    def _predict_performance(self, 
                           operation_type: str, 
                           input_data: Dict[str, Any], 
                           context: Dict[str, Any]) -> float:
        """Predice el rendimiento de una operación"""
        
        try:
            if self.models['performance_predictor']:
                return self.models['performance_predictor'].predict(
                    operation_type, input_data, context
                )
            else:
                # Predicción básica
                return self._basic_performance_prediction(operation_type, input_data, context)
                
        except Exception as e:
            logger.error(f"❌ Error prediciendo rendimiento: {e}")
            return 1.0  # Rendimiento base
    
    def _basic_performance_prediction(self, 
                                    operation_type: str, 
                                    input_data: Dict[str, Any], 
                                    context: Dict[str, Any]) -> float:
        """Predicción básica de rendimiento"""
        
        # Factores básicos
        cpu_factor = 1.0 - (context.get('cpu_usage', 0) / 100)
        memory_factor = 1.0 - (context.get('memory_usage', 0) / 100)
        
        # Factor de tipo de operación
        operation_factors = {
            'image_processing': 0.8,
            'file_compression': 0.9,
            'data_processing': 0.7,
            'batch_operation': 0.6
        }
        
        operation_factor = operation_factors.get(operation_type, 0.5)
        
        # Factor de tamaño de datos
        data_size = input_data.get('data_size', 1)
        size_factor = 1.0 / (1.0 + (data_size / (1024 * 1024)))  # MB
        
        # Rendimiento predicho
        predicted_performance = cpu_factor * memory_factor * operation_factor * size_factor
        
        return max(0.1, min(1.0, predicted_performance))
    
    def _select_optimal_strategy(self, 
                                operation_type: str,
                                input_data: Dict[str, Any],
                                context: Dict[str, Any],
                                current_performance: float) -> OptimizationStrategy:
        """Selecciona la estrategia óptima"""
        
        try:
            if self.models['strategy_selector']:
                return self.models['strategy_selector'].select_strategy(
                    operation_type, input_data, context, current_performance
                )
            else:
                return self._basic_strategy_selection(operation_type, input_data, context, current_performance)
                
        except Exception as e:
            logger.error(f"❌ Error seleccionando estrategia: {e}")
            return OptimizationStrategy.BALANCED
    
    def _basic_strategy_selection(self, 
                                 operation_type: str,
                                 input_data: Dict[str, Any],
                                 context: Dict[str, Any],
                                 current_performance: float) -> OptimizationStrategy:
        """Selección básica de estrategia"""
        
        # Si el rendimiento es muy bajo, priorizar velocidad
        if current_performance < 0.3:
            return OptimizationStrategy.SPEED_FIRST
        
        # Si hay muchos recursos disponibles, priorizar calidad
        if (context.get('cpu_usage', 100) < 30 and 
            context.get('memory_usage', 100) < 50):
            return OptimizationStrategy.QUALITY_FIRST
        
        # Si es una operación crítica, usar balanceado
        if operation_type in ['critical_processing', 'user_facing']:
            return OptimizationStrategy.BALANCED
        
        # Por defecto, usar adaptativo
        return OptimizationStrategy.ADAPTIVE
    
    def _optimize_parameters(self, 
                            strategy: OptimizationStrategy,
                            input_data: Dict[str, Any],
                            context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimiza parámetros según la estrategia"""
        
        try:
            if self.models['parameter_optimizer']:
                return self.models['parameter_optimizer'].optimize_parameters(
                    strategy, input_data, context
                )
            else:
                return self._basic_parameter_optimization(strategy, input_data, context)
                
        except Exception as e:
            logger.error(f"❌ Error optimizando parámetros: {e}")
            return self.current_config.copy()
    
    def _basic_parameter_optimization(self, 
                                    strategy: OptimizationStrategy,
                                    input_data: Dict[str, Any],
                                    context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimización básica de parámetros"""
        
        params = self.current_config.copy()
        
        if strategy == OptimizationStrategy.SPEED_FIRST:
            # Máxima velocidad
            params['max_workers'] = min(32, os.cpu_count() * 4)
            params['chunk_size'] = 10
            params['compression_level'] = 'ultra_fast'
            params['cache_size'] = 500
            params['parallel_processing'] = True
            params['adaptive_quality'] = False
            
        elif strategy == OptimizationStrategy.QUALITY_FIRST:
            # Máxima calidad
            params['max_workers'] = max(4, os.cpu_count())
            params['chunk_size'] = 50
            params['compression_level'] = 'maximum'
            params['cache_size'] = 2000
            params['parallel_processing'] = True
            params['adaptive_quality'] = True
            
        elif strategy == OptimizationStrategy.BALANCED:
            # Equilibrio
            params['max_workers'] = min(16, os.cpu_count() * 2)
            params['chunk_size'] = 25
            params['compression_level'] = 'balanced'
            params['cache_size'] = 1000
            params['parallel_processing'] = True
            params['adaptive_quality'] = True
            
        elif strategy == OptimizationStrategy.ADAPTIVE:
            # Adaptativo según contexto
            cpu_usage = context.get('cpu_usage', 50)
            memory_usage = context.get('memory_usage', 50)
            
            if cpu_usage > 80 or memory_usage > 80:
                # Sistema sobrecargado, priorizar velocidad
                params['max_workers'] = max(2, os.cpu_count() // 2)
                params['chunk_size'] = 15
                params['compression_level'] = 'fast'
            else:
                # Sistema con recursos, priorizar calidad
                params['max_workers'] = min(24, os.cpu_count() * 3)
                params['chunk_size'] = 35
                params['compression_level'] = 'balanced'
        
        return params
    
    def _calculate_expected_improvement(self, 
                                      current_performance: float,
                                      strategy: OptimizationStrategy,
                                      params: Dict[str, Any]) -> float:
        """Calcula la mejora esperada"""
        
        # Factores de mejora por estrategia
        improvement_factors = {
            OptimizationStrategy.SPEED_FIRST: 2.5,
            OptimizationStrategy.BALANCED: 1.8,
            OptimizationStrategy.QUALITY_FIRST: 1.3,
            OptimizationStrategy.ADAPTIVE: 2.0,
            OptimizationStrategy.LEARNING: 3.0
        }
        
        base_improvement = improvement_factors.get(strategy, 1.5)
        
        # Ajustar según parámetros
        worker_factor = min(params.get('max_workers', 8) / 8, 2.0)
        cache_factor = min(params.get('cache_size', 1000) / 1000, 1.5)
        
        total_improvement = base_improvement * worker_factor * cache_factor
        
        # Limitar mejora máxima
        return min(total_improvement, 5.0)
    
    def _calculate_confidence(self, 
                            strategy: OptimizationStrategy,
                            params: Dict[str, Any]) -> float:
        """Calcula la confianza en la optimización"""
        
        # Confianza base por estrategia
        base_confidence = {
            OptimizationStrategy.SPEED_FIRST: 0.8,
            OptimizationStrategy.BALANCED: 0.9,
            OptimizationStrategy.QUALITY_FIRST: 0.85,
            OptimizationStrategy.ADAPTIVE: 0.7,
            OptimizationStrategy.LEARNING: 0.95
        }
        
        confidence = base_confidence.get(strategy, 0.7)
        
        # Ajustar según historial de decisiones exitosas
        if self.decision_history:
            successful_decisions = [
                d for d in self.decision_history[-10:]  # Últimas 10 decisiones
                if d.expected_improvement > 0
            ]
            
            if successful_decisions:
                success_rate = len(successful_decisions) / 10
                confidence += success_rate * 0.2
        
        return min(1.0, confidence)
    
    def _generate_reasoning(self, 
                           strategy: OptimizationStrategy,
                           params: Dict[str, Any],
                           expected_improvement: float) -> str:
        """Genera explicación de la optimización"""
        
        reasoning_parts = [
            f"Estrategia seleccionada: {strategy.value}",
            f"Workers configurados: {params.get('max_workers', 8)}",
            f"Tamaño de chunk: {params.get('chunk_size', 25)}",
            f"Nivel de compresión: {params.get('compression_level', 'balanced')}",
            f"Procesamiento paralelo: {'Sí' if params.get('parallel_processing', True) else 'No'}",
            f"Mejora esperada: {expected_improvement:.1f}x"
        ]
        
        return " | ".join(reasoning_parts)
    
    def _apply_optimization(self, decision: OptimizationDecision):
        """Aplica la optimización"""
        
        try:
            # Actualizar configuración actual
            self.current_config.update(decision.parameters)
            
            # Aplicar cambios al sistema
            self._apply_system_changes(decision.parameters)
            
            logger.info(f"⚡ Optimización aplicada: {decision.strategy.value}")
            
        except Exception as e:
            logger.error(f"❌ Error aplicando optimización: {e}")
    
    def _apply_system_changes(self, params: Dict[str, Any]):
        """Aplica cambios al sistema"""
        
        try:
            # Aquí se aplicarían los cambios reales al sistema
            # Por ejemplo, cambiar número de workers, tamaño de caché, etc.
            
            # Simular aplicación de cambios
            time.sleep(0.01)
            
        except Exception as e:
            logger.error(f"❌ Error aplicando cambios del sistema: {e}")
    
    def record_performance(self, 
                          metric: PerformanceMetric,
                          value: float,
                          context: Dict[str, Any] = None):
        """Registra métrica de rendimiento"""
        
        try:
            performance_data = PerformanceData(
                metric=metric,
                value=value,
                timestamp=time.time(),
                context=context or {}
            )
            
            with self.db_lock:
                self.performance_db.append(performance_data)
                
                # Mantener solo las últimas 10000 métricas
                if len(self.performance_db) > 10000:
                    self.performance_db = self.performance_db[-10000:]
            
        except Exception as e:
            logger.error(f"❌ Error registrando métrica: {e}")
    
    def _learn_from_data(self):
        """Aprende de los datos recopilados"""
        
        try:
            if not self.performance_db or len(self.performance_db) < 100:
                return
            
            # Analizar tendencias
            trends = self._analyze_trends()
            
            # Actualizar modelos
            self._update_models(trends)
            
            # Guardar modelos
            self._save_models()
            
            self.metrics['learning_cycles'] += 1
            logger.info(f"🧠 Ciclo de aprendizaje completado: {self.metrics['learning_cycles']}")
            
        except Exception as e:
            logger.error(f"❌ Error en aprendizaje: {e}")
    
    def _analyze_trends(self) -> Dict[str, Any]:
        """Analiza tendencias en los datos"""
        
        try:
            # Convertir a DataFrame para análisis
            df = pd.DataFrame([
                {
                    'metric': p.metric.value,
                    'value': p.value,
                    'timestamp': p.timestamp,
                    'cpu_usage': p.context.get('cpu_usage', 0),
                    'memory_usage': p.context.get('memory_usage', 0)
                }
                for p in self.performance_db
            ])
            
            if df.empty:
                return {}
            
            # Agregar timestamp como datetime
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
            
            # Análisis por métrica
            trends = {}
            for metric in PerformanceMetric:
                metric_data = df[df['metric'] == metric.value]
                if not metric_data.empty:
                    trends[metric.value] = {
                        'mean': metric_data['value'].mean(),
                        'std': metric_data['value'].std(),
                        'trend': self._calculate_trend(metric_data['value']),
                        'correlation_cpu': metric_data['value'].corr(metric_data['cpu_usage']),
                        'correlation_memory': metric_data['value'].corr(metric_data['memory_usage'])
                    }
            
            return trends
            
        except Exception as e:
            logger.error(f"❌ Error analizando tendencias: {e}")
            return {}
    
    def _calculate_trend(self, values: pd.Series) -> str:
        """Calcula tendencia de una serie de valores"""
        
        try:
            if len(values) < 2:
                return 'stable'
            
            # Regresión lineal simple
            x = np.arange(len(values))
            slope = np.polyfit(x, values, 1)[0]
            
            if slope > 0.01:
                return 'improving'
            elif slope < -0.01:
                return 'declining'
            else:
                return 'stable'
                
        except Exception:
            return 'stable'
    
    def _update_models(self, trends: Dict[str, Any]):
        """Actualiza modelos con nuevas tendencias"""
        
        try:
            # Aquí se actualizarían los modelos reales
            # Por ahora solo simulamos la actualización
            
            for model_name in self.models.keys():
                if self.models[model_name] and hasattr(self.models[model_name], 'update'):
                    self.models[model_name].update(trends)
            
        except Exception as e:
            logger.error(f"❌ Error actualizando modelos: {e}")
    
    def _save_models(self):
        """Guarda modelos actualizados"""
        
        try:
            for model_name, model in self.models.items():
                if model:
                    model_file = os.path.join(self.model_path, f"{model_name}.pkl")
                    with open(model_file, 'wb') as f:
                        pickle.dump(model, f)
            
            logger.info("💾 Modelos guardados")
            
        except Exception as e:
            logger.error(f"❌ Error guardando modelos: {e}")
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de optimización"""
        
        return {
            'metrics': self.metrics.copy(),
            'current_config': self.current_config.copy(),
            'recent_decisions': [
                {
                    'strategy': d.strategy.value,
                    'confidence': d.confidence,
                    'improvement': d.expected_improvement,
                    'timestamp': d.timestamp
                }
                for d in self.decision_history[-10:]  # Últimas 10 decisiones
            ],
            'performance_trends': self._analyze_trends() if self.performance_db else {}
        }

# Modelos básicos
class SimplePerformancePredictor:
    """Predictor simple de rendimiento"""
    
    def predict(self, operation_type: str, input_data: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Predice rendimiento"""
        # Implementación básica
        return 0.7

class BasicStrategySelector:
    """Selector básico de estrategia"""
    
    def select_strategy(self, operation_type: str, input_data: Dict[str, Any], context: Dict[str, Any], current_performance: float) -> OptimizationStrategy:
        """Selecciona estrategia"""
        # Implementación básica
        return OptimizationStrategy.BALANCED

class BasicParameterOptimizer:
    """Optimizador básico de parámetros"""
    
    def optimize_parameters(self, strategy: OptimizationStrategy, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimiza parámetros"""
        # Implementación básica
        return {
            'max_workers': 8,
            'chunk_size': 25,
            'compression_level': 'balanced'
        }

# Función para crear optimizador de IA
def create_ai_optimizer(enable_learning: bool = True,
                       model_path: str = 'ai_models') -> AIOptimizer:
    """Crea una instancia del optimizador de IA"""
    
    try:
        optimizer = AIOptimizer(
            enable_learning=enable_learning,
            model_path=model_path
        )
        
        logger.info("✅ Optimizador de IA creado exitosamente")
        return optimizer
        
    except Exception as e:
        logger.error(f"❌ Error creando optimizador de IA: {e}")
        return None

if __name__ == "__main__":
    # Crear y probar el optimizador de IA
    logger.info("🤖 Probando optimizador de IA")
    
    optimizer = create_ai_optimizer()
    if optimizer:
        # Simular operación
        input_data = {
            'operation_type': 'image_processing',
            'data_size': 1024 * 1024,  # 1MB
            'file_count': 10
        }
        
        # Optimizar operación
        decision = optimizer.optimize_operation('image_processing', input_data)
        
        logger.info(f"🎯 Estrategia seleccionada: {decision.strategy.value}")
        logger.info(f"🎯 Parámetros: {decision.parameters}")
        logger.info(f"🎯 Confianza: {decision.confidence:.2f}")
        logger.info(f"🎯 Mejora esperada: {decision.expected_improvement:.1f}x")
        logger.info(f"🎯 Razón: {decision.reasoning}")
        
        # Mostrar estadísticas
        stats = optimizer.get_optimization_stats()
        logger.info(f"📊 Estadísticas: {stats}")
        
    else:
        logger.error("❌ No se pudo crear el optimizador de IA") 