#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador Especializado para Diseño de Solución - Fangio Telecom
Velocidad extrema para diseños de soluciones
"""

import os
import time
import json
import logging
import asyncio
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import pandas as pd
import numpy as np
import hashlib
import queue
import multiprocessing as mp

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fangio_solution_design.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SolutionType(Enum):
    """Tipos de solución"""
    PTP = 'ptp'                    # Point to Point
    PTMP = 'ptmp'                  # Point to Multipoint
    WIFI = 'wifi'                  # WiFi
    FIBER = 'fiber'                # Fibra óptica
    HYBRID = 'hybrid'              # Híbrido
    CLOUD = 'cloud'                # Solución en la nube

class DesignPriority(Enum):
    """Prioridades de diseño"""
    CRITICAL = 1                   # Crítico (máxima prioridad)
    HIGH = 2                       # Alto
    NORMAL = 3                     # Normal
    LOW = 4                        # Bajo

@dataclass
class SolutionDesignData:
    """Datos del diseño de solución"""
    design_id: str
    solution_type: SolutionType
    requirements: Dict[str, Any]
    site_survey_data: Dict[str, Any]
    budget_constraints: Dict[str, Any]
    timeline: Dict[str, Any]
    priority: DesignPriority
    timestamp: float

@dataclass
class DesignResult:
    """Resultado del diseño"""
    design_id: str
    success: bool
    processing_time: float
    output_files: List[str]
    quality_score: float
    cost_estimate: float
    timeline_estimate: str
    errors: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

class SolutionDesignProcessor:
    """Procesador especializado para Diseño de Solución con máxima velocidad"""
    
    def __init__(self, 
                 max_workers: int = 24,
                 enable_gpu: bool = False,
                 enable_parallel: bool = True,
                 cache_enabled: bool = True):
        
        self.max_workers = max_workers
        self.enable_gpu = enable_gpu
        self.enable_parallel = enable_parallel
        self.cache_enabled = cache_enabled
        
        # Pools de ejecución
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self.process_pool = ProcessPoolExecutor(max_workers=max_workers // 2)
        
        # Cola prioritaria de trabajos
        self.job_queue = queue.PriorityQueue()
        
        # Caché de resultados
        self.result_cache = {}
        self.cache_lock = threading.Lock()
        
        # Estadísticas de rendimiento
        self.stats = {
            'designs_processed': 0,
            'total_processing_time': 0,
            'average_processing_time': 0,
            'success_rate': 0.0,
            'total_cost_estimated': 0.0
        }
        
        # Configuración especializada por tipo de solución
        self.solution_configs = self._get_solution_configs()
        
        # Iniciar workers
        self._start_workers()
        
        logger.info(f"🚀 Procesador de Diseño de Solución iniciado con {max_workers} workers")
    
    def _get_solution_configs(self) -> Dict[SolutionType, Dict[str, Any]]:
        """Obtiene configuraciones especializadas por tipo de solución"""
        
        return {
            SolutionType.PTP: {
                'equipment_selection': True,
                'path_loss_calculation': True,
                'fresnel_zone_analysis': True,
                'equipment_configuration': True,
                'priority_boost': 1.5
            },
            SolutionType.PTMP: {
                'equipment_selection': True,
                'coverage_planning': True,
                'capacity_planning': True,
                'interference_mitigation': True,
                'priority_boost': 1.3
            },
            SolutionType.WIFI: {
                'access_point_selection': True,
                'coverage_mapping': True,
                'channel_planning': True,
                'security_configuration': True,
                'priority_boost': 1.2
            },
            SolutionType.FIBER: {
                'cable_selection': True,
                'route_planning': True,
                'splicing_plan': True,
                'testing_procedures': True,
                'priority_boost': 1.4
            },
            SolutionType.HYBRID: {
                'technology_integration': True,
                'interoperability': True,
                'redundancy_planning': True,
                'migration_strategy': True,
                'priority_boost': 1.6
            },
            SolutionType.CLOUD: {
                'cloud_provider_selection': True,
                'architecture_design': True,
                'scalability_planning': True,
                'security_architecture': True,
                'priority_boost': 1.1
            }
        }
    
    def _start_workers(self):
        """Inicia workers especializados"""
        self.workers = []
        
        # Workers de proceso para tareas pesadas
        for i in range(self.max_workers // 2):
            worker = mp.Process(target=self._process_worker, args=(i,))
            worker.start()
            self.workers.append(worker)
        
        # Workers de thread para tareas ligeras
        for i in range(self.max_workers):
            thread = threading.Thread(target=self._thread_worker, args=(i,))
            thread.daemon = True
            thread.start()
            self.workers.append(thread)
    
    def _process_worker(self, worker_id: int):
        """Worker de proceso para tareas pesadas de diseño"""
        logger.info(f"🔄 Proceso worker {worker_id} iniciado para Diseño de Solución")
        
        while True:
            try:
                job = self.job_queue.get(timeout=1)
                if job is None:
                    break
                
                self._execute_design_job(job, worker_id)
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ Error en proceso worker {worker_id}: {e}")
    
    def _thread_worker(self, worker_id: int):
        """Worker de thread para tareas ligeras de diseño"""
        logger.info(f"🧵 Thread worker {worker_id} iniciado para Diseño de Solución")
        
        while True:
            try:
                job = self.job_queue.get(timeout=1)
                if job is None:
                    break
                
                self._execute_design_job(job, worker_id)
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ Error en thread worker {worker_id}: {e}")
    
    def _execute_design_job(self, job: Tuple[int, SolutionDesignData], worker_id: int):
        """Ejecuta un trabajo de diseño"""
        priority, design_data = job
        start_time = time.time()
        
        try:
            logger.info(f"🚀 Procesando diseño {design_data.design_id} en worker {worker_id}")
            
            # Procesar según el tipo de solución
            result = self._process_solution_by_type(design_data)
            
            # Actualizar estadísticas
            processing_time = time.time() - start_time
            self._update_stats(result, processing_time)
            
            # Guardar en caché si está habilitado
            if self.cache_enabled:
                self._cache_result(design_data.design_id, result)
            
            logger.info(f"✅ Diseño {design_data.design_id} completado en {processing_time:.2f}s")
            
        except Exception as e:
            logger.error(f"❌ Error procesando diseño {design_data.design_id}: {e}")
    
    def _process_solution_by_type(self, design_data: SolutionDesignData) -> DesignResult:
        """Procesa una solución según su tipo"""
        
        start_time = time.time()
        config = self.solution_configs[design_data.solution_type]
        
        try:
            output_files = []
            errors = []
            recommendations = []
            
            # Procesamiento específico según tipo
            if design_data.solution_type == SolutionType.PTP:
                ptp_results = self._process_ptp_solution(design_data)
                output_files.extend(ptp_results['files'])
                errors.extend(ptp_results['errors'])
                recommendations.extend(ptp_results['recommendations'])
            
            elif design_data.solution_type == SolutionType.PTMP:
                ptmp_results = self._process_ptmp_solution(design_data)
                output_files.extend(ptmp_results['files'])
                errors.extend(ptmp_results['errors'])
                recommendations.extend(ptmp_results['recommendations'])
            
            elif design_data.solution_type == SolutionType.WIFI:
                wifi_results = self._process_wifi_solution(design_data)
                output_files.extend(wifi_results['files'])
                errors.extend(wifi_results['errors'])
                recommendations.extend(wifi_results['recommendations'])
            
            elif design_data.solution_type == SolutionType.FIBER:
                fiber_results = self._process_fiber_solution(design_data)
                output_files.extend(fiber_results['files'])
                errors.extend(fiber_results['errors'])
                recommendations.extend(fiber_results['recommendations'])
            
            elif design_data.solution_type == SolutionType.HYBRID:
                hybrid_results = self._process_hybrid_solution(design_data)
                output_files.extend(hybrid_results['files'])
                errors.extend(hybrid_results['errors'])
                recommendations.extend(hybrid_results['recommendations'])
            
            elif design_data.solution_type == SolutionType.CLOUD:
                cloud_results = self._process_cloud_solution(design_data)
                output_files.extend(cloud_results['files'])
                errors.extend(cloud_results['errors'])
                recommendations.extend(cloud_results['recommendations'])
            
            # Generar documentación final
            doc_file = self._generate_solution_documentation(design_data, output_files)
            output_files.append(doc_file)
            
            # Generar presupuesto
            budget_file = self._generate_budget_estimate(design_data, output_files)
            output_files.append(budget_file)
            
            processing_time = time.time() - start_time
            quality_score = self._calculate_quality_score(design_data, output_files, errors)
            cost_estimate = self._calculate_cost_estimate(design_data, output_files)
            timeline_estimate = self._calculate_timeline_estimate(design_data, output_files)
            
            return DesignResult(
                design_id=design_data.design_id,
                success=len(errors) == 0,
                processing_time=processing_time,
                output_files=output_files,
                quality_score=quality_score,
                cost_estimate=cost_estimate,
                timeline_estimate=timeline_estimate,
                errors=errors,
                recommendations=recommendations
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return DesignResult(
                design_id=design_data.design_id,
                success=False,
                processing_time=processing_time,
                output_files=[],
                quality_score=0.0,
                cost_estimate=0.0,
                timeline_estimate="Error",
                errors=[str(e)]
            )
    
    def _process_ptp_solution(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Procesa solución PTP"""
        
        results = {
            'files': [],
            'errors': [],
            'recommendations': []
        }
        
        try:
            # Selección de equipos
            equipment_file = f"ptp_equipment_{design_data.design_id}.json"
            equipment_data = {
                'design_id': design_data.design_id,
                'antennas': self._select_ptp_antennas(design_data),
                'radios': self._select_ptp_radios(design_data),
                'cables': self._select_ptp_cables(design_data),
                'mounts': self._select_ptp_mounts(design_data),
                'timestamp': time.time()
            }
            
            with open(equipment_file, 'w') as f:
                json.dump(equipment_data, f, indent=2)
            
            results['files'].append(equipment_file)
            
            # Análisis de pérdida de trayectoria
            pathloss_file = f"ptp_pathloss_{design_data.design_id}.json"
            pathloss_data = {
                'design_id': design_data.design_id,
                'path_loss_db': self._calculate_path_loss(design_data),
                'fresnel_zone_m': self._calculate_fresnel_zone(design_data),
                'link_budget': self._calculate_link_budget(design_data),
                'timestamp': time.time()
            }
            
            with open(pathloss_file, 'w') as f:
                json.dump(pathloss_data, f, indent=2)
            
            results['files'].append(pathloss_file)
            
            # Recomendaciones
            results['recommendations'].extend([
                "Usar antenas de alta ganancia para distancias largas",
                "Implementar diversidad de polarización",
                "Considerar backup de energía"
            ])
            
        except Exception as e:
            results['errors'].append(f"Error procesando PTP: {e}")
        
        return results
    
    def _process_ptmp_solution(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Procesa solución PTMP"""
        
        results = {
            'files': [],
            'errors': [],
            'recommendations': []
        }
        
        try:
            # Planificación de cobertura
            coverage_file = f"ptmp_coverage_{design_data.design_id}.json"
            coverage_data = {
                'design_id': design_data.design_id,
                'coverage_radius_km': 5.0,
                'sector_angles': [60, 60, 60, 60, 60, 60],  # 6 sectores
                'capacity_per_sector': '100 Mbps',
                'total_capacity': '600 Mbps',
                'timestamp': time.time()
            }
            
            with open(coverage_file, 'w') as f:
                json.dump(coverage_data, f, indent=2)
            
            results['files'].append(coverage_file)
            
            # Recomendaciones
            results['recommendations'].extend([
                "Implementar sectores de 60° para máxima cobertura",
                "Usar MIMO 2x2 para mayor capacidad",
                "Considerar QoS por sector"
            ])
            
        except Exception as e:
            results['errors'].append(f"Error procesando PTMP: {e}")
        
        return results
    
    def _process_wifi_solution(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Procesa solución WiFi"""
        
        results = {
            'files': [],
            'errors': [],
            'recommendations': []
        }
        
        try:
            # Selección de Access Points
            ap_file = f"wifi_aps_{design_data.design_id}.json"
            ap_data = {
                'design_id': design_data.design_id,
                'access_points': self._select_wifi_aps(design_data),
                'coverage_map': self._generate_wifi_coverage_map(design_data),
                'channel_plan': self._create_wifi_channel_plan(design_data),
                'security_config': self._configure_wifi_security(design_data),
                'timestamp': time.time()
            }
            
            with open(ap_file, 'w') as f:
                json.dump(ap_data, f, indent=2)
            
            results['files'].append(ap_file)
            
            # Recomendaciones
            results['recommendations'].extend([
                "Usar WiFi 6 para mayor capacidad",
                "Implementar roaming seamless",
                "Configurar VLANs por tipo de usuario"
            ])
            
        except Exception as e:
            results['errors'].append(f"Error procesando WiFi: {e}")
        
        return results
    
    def _process_fiber_solution(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Procesa solución de Fibra"""
        
        results = {
            'files': [],
            'errors': [],
            'recommendations': []
        }
        
        try:
            # Selección de cable
            cable_file = f"fiber_cable_{design_data.design_id}.json"
            cable_data = {
                'design_id': design_data.design_id,
                'cable_type': 'Single Mode OS2',
                'fiber_count': 12,
                'route_length_km': 2.5,
                'splicing_points': 5,
                'testing_procedures': self._define_fiber_testing(design_data),
                'timestamp': time.time()
            }
            
            with open(cable_file, 'w') as f:
                json.dump(cable_data, f, indent=2)
            
            results['files'].append(cable_file)
            
            # Recomendaciones
            results['recommendations'].extend([
                "Usar cable armado para exteriores",
                "Implementar redundancia de fibras",
                "Documentar cada punto de empalme"
            ])
            
        except Exception as e:
            results['errors'].append(f"Error procesando Fibra: {e}")
        
        return results
    
    def _process_hybrid_solution(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Procesa solución Híbrida"""
        
        results = {
            'files': [],
            'errors': [],
            'recommendations': []
        }
        
        try:
            # Integración de tecnologías
            integration_file = f"hybrid_integration_{design_data.design_id}.json"
            integration_data = {
                'design_id': design_data.design_id,
                'technologies': ['Fiber', 'Wireless', 'WiFi'],
                'integration_points': self._define_integration_points(design_data),
                'redundancy_plan': self._create_redundancy_plan(design_data),
                'migration_strategy': self._plan_migration_strategy(design_data),
                'timestamp': time.time()
            }
            
            with open(integration_file, 'w') as f:
                json.dump(integration_data, f, indent=2)
            
            results['files'].append(integration_file)
            
            # Recomendaciones
            results['recommendations'].extend([
                "Implementar gateway de integración",
                "Planificar migración gradual",
                "Mantener compatibilidad hacia atrás"
            ])
            
        except Exception as e:
            results['errors'].append(f"Error procesando Híbrida: {e}")
        
        return results
    
    def _process_cloud_solution(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Procesa solución en la Nube"""
        
        results = {
            'files': [],
            'errors': [],
            'recommendations': []
        }
        
        try:
            # Arquitectura en la nube
            cloud_file = f"cloud_architecture_{design_data.design_id}.json"
            cloud_data = {
                'design_id': design_data.design_id,
                'cloud_provider': 'AWS',
                'architecture': self._design_cloud_architecture(design_data),
                'scalability_plan': self._plan_cloud_scalability(design_data),
                'security_architecture': self._design_cloud_security(design_data),
                'timestamp': time.time()
            }
            
            with open(cloud_file, 'w') as f:
                json.dump(cloud_data, f, indent=2)
            
            results['files'].append(cloud_file)
            
            # Recomendaciones
            results['recommendations'].extend([
                "Implementar auto-scaling",
                "Usar múltiples regiones",
                "Implementar backup automático"
            ])
            
        except Exception as e:
            results['errors'].append(f"Error procesando Nube: {e}")
        
        return results
    
    # Métodos auxiliares para cálculos y selecciones
    def _select_ptp_antennas(self, design_data: SolutionDesignData) -> List[Dict[str, Any]]:
        """Selecciona antenas PTP"""
        return [
            {'type': 'Parabólica', 'gain_dbi': 30, 'frequency_ghz': 5.8},
            {'type': 'Grid', 'gain_dbi': 28, 'frequency_ghz': 5.8}
        ]
    
    def _select_ptp_radios(self, design_data: SolutionDesignData) -> List[Dict[str, Any]]:
        """Selecciona radios PTP"""
        return [
            {'model': 'Mikrotik NetMetal 5', 'power_w': 1, 'data_rate': '1 Gbps'},
            {'model': 'Ubiquiti PowerBeam 5AC', 'power_w': 0.5, 'data_rate': '450 Mbps'}
        ]
    
    def _calculate_path_loss(self, design_data: SolutionDesignData) -> float:
        """Calcula pérdida de trayectoria"""
        # Fórmula simplificada
        distance_km = 1.0  # Valor por defecto
        frequency_ghz = 5.8
        return 92.45 + 20 * np.log10(distance_km) + 20 * np.log10(frequency_ghz)
    
    def _calculate_fresnel_zone(self, design_data: SolutionDesignData) -> float:
        """Calcula zona de Fresnel"""
        distance_km = 1.0  # Valor por defecto
        frequency_ghz = 5.8
        return 17.3 * np.sqrt(distance_km / (4 * frequency_ghz))
    
    def _calculate_link_budget(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Calcula presupuesto del enlace"""
        return {
            'transmit_power_dbm': 30,
            'antenna_gain_dbi': 30,
            'path_loss_db': -120,
            'receive_sensitivity_dbm': -85,
            'fade_margin_db': 15
        }
    
    def _select_wifi_aps(self, design_data: SolutionDesignData) -> List[Dict[str, Any]]:
        """Selecciona Access Points WiFi"""
        return [
            {'model': 'Cisco Aironet 2800', 'standard': 'WiFi 6', 'coverage_m2': 500},
            {'model': 'Ubiquiti UniFi AP-AC-PRO', 'standard': 'WiFi 5', 'coverage_m2': 400}
        ]
    
    def _generate_wifi_coverage_map(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Genera mapa de cobertura WiFi"""
        return {
            'total_area_m2': 2000,
            'ap_count': 4,
            'coverage_per_ap_m2': 500,
            'overlap_percentage': 20
        }
    
    def _create_wifi_channel_plan(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Crea plan de canales WiFi"""
        return {
            '2.4ghz_channels': [1, 6, 11],
            '5ghz_channels': [36, 40, 44, 48, 149, 153, 157, 161],
            'channel_width_mhz': 40
        }
    
    def _configure_wifi_security(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Configura seguridad WiFi"""
        return {
            'encryption': 'WPA3',
            'authentication': '802.1X',
            'radius_server': 'Local',
            'vlan_assignment': True
        }
    
    def _define_fiber_testing(self, design_data: SolutionDesignData) -> List[str]:
        """Define procedimientos de prueba de fibra"""
        return [
            'OTDR testing',
            'Power meter testing',
            'Visual fault locator',
            'End face inspection'
        ]
    
    def _define_integration_points(self, design_data: SolutionDesignData) -> List[Dict[str, Any]]:
        """Define puntos de integración"""
        return [
            {'technology': 'Fiber', 'interface': 'SFP+', 'speed': '10 Gbps'},
            {'technology': 'Wireless', 'interface': 'Ethernet', 'speed': '1 Gbps'},
            {'technology': 'WiFi', 'interface': 'Ethernet', 'speed': '1 Gbps'}
        ]
    
    def _create_redundancy_plan(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Crea plan de redundancia"""
        return {
            'primary_path': 'Fiber',
            'backup_path': 'Wireless',
            'failover_time_ms': 50,
            'load_balancing': True
        }
    
    def _plan_migration_strategy(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Planifica estrategia de migración"""
        return {
            'phase_1': 'Infraestructura base',
            'phase_2': 'Migración gradual',
            'phase_3': 'Optimización',
            'rollback_plan': 'Disponible'
        }
    
    def _design_cloud_architecture(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Diseña arquitectura en la nube"""
        return {
            'compute': 'EC2 Auto Scaling Groups',
            'storage': 'S3 + EBS',
            'database': 'RDS Multi-AZ',
            'load_balancer': 'ALB + NLB'
        }
    
    def _plan_cloud_scalability(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Planifica escalabilidad en la nube"""
        return {
            'auto_scaling': True,
            'min_instances': 2,
            'max_instances': 20,
            'scaling_policies': 'CPU + Memory based'
        }
    
    def _design_cloud_security(self, design_data: SolutionDesignData) -> Dict[str, Any]:
        """Diseña seguridad en la nube"""
        return {
            'vpc': 'Private subnets only',
            'security_groups': 'Restrictive rules',
            'iam': 'Least privilege access',
            'encryption': 'At rest and in transit'
        }
    
    def _generate_solution_documentation(self, design_data: SolutionDesignData, output_files: List[str]) -> str:
        """Genera documentación de la solución"""
        
        try:
            doc_file = f"solution_documentation_{design_data.design_id}.html"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Diseño de Solución - {design_data.design_id}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background: #e3f2fd; padding: 20px; border-radius: 5px; }}
                    .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
                    .file-list {{ background: #f9f9f9; padding: 10px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🎯 Diseño de Solución</h1>
                    <h2>ID: {design_data.design_id}</h2>
                    <p><strong>Tipo:</strong> {design_data.solution_type.value.upper()}</p>
                    <p><strong>Prioridad:</strong> {design_data.priority.value}</p>
                    <p><strong>Fecha:</strong> {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(design_data.timestamp))}</p>
                </div>
                
                <div class="section">
                    <h3>📊 Resumen del Diseño</h3>
                    <p><strong>Archivos generados:</strong> {len(output_files)}</p>
                    <p><strong>Requisitos analizados:</strong> {len(design_data.requirements)}</p>
                    <p><strong>Restricciones de presupuesto:</strong> {len(design_data.budget_constraints)}</p>
                </div>
                
                <div class="section">
                    <h3>📁 Archivos de Salida</h3>
                    <div class="file-list">
                        {''.join([f'<p>• {os.path.basename(f)}</p>' for f in output_files])}
                    </div>
                </div>
                
                <div class="section">
                    <h3>🎯 Próximos Pasos</h3>
                    <p>1. Revisar documentación generada</p>
                    <p>2. Validar presupuesto estimado</p>
                    <p>3. Confirmar cronograma</p>
                    <p>4. Iniciar implementación</p>
                </div>
            </body>
            </html>
            """
            
            with open(doc_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return doc_file
            
        except Exception as e:
            logger.error(f"❌ Error generando documentación: {e}")
            return ""
    
    def _generate_budget_estimate(self, design_data: SolutionDesignData, output_files: List[str]) -> str:
        """Genera estimación de presupuesto"""
        
        try:
            budget_file = f"budget_estimate_{design_data.design_id}.json"
            
            # Calcular presupuesto basado en tipo de solución
            base_costs = {
                SolutionType.PTP: 5000,
                SolutionType.PTMP: 15000,
                SolutionType.WIFI: 8000,
                SolutionType.FIBER: 25000,
                SolutionType.HYBRID: 35000,
                SolutionType.CLOUD: 12000
            }
            
            base_cost = base_costs.get(design_data.solution_type, 10000)
            
            # Ajustar por requisitos
            requirements_multiplier = 1.0 + (len(design_data.requirements) * 0.1)
            
            # Ajustar por restricciones de presupuesto
            budget_constraint_multiplier = 0.8 if design_data.budget_constraints.get('strict', False) else 1.0
            
            total_cost = base_cost * requirements_multiplier * budget_constraint_multiplier
            
            budget_data = {
                'design_id': design_data.design_id,
                'base_cost_usd': base_cost,
                'requirements_multiplier': requirements_multiplier,
                'budget_constraint_multiplier': budget_constraint_multiplier,
                'total_estimated_cost_usd': total_cost,
                'breakdown': {
                    'equipment': total_cost * 0.6,
                    'installation': total_cost * 0.25,
                    'testing': total_cost * 0.10,
                    'documentation': total_cost * 0.05
                },
                'timestamp': time.time()
            }
            
            with open(budget_file, 'w') as f:
                json.dump(budget_data, f, indent=2)
            
            return budget_file
            
        except Exception as e:
            logger.error(f"❌ Error generando presupuesto: {e}")
            return ""
    
    def _calculate_cost_estimate(self, design_data: SolutionDesignData, output_files: List[str]) -> float:
        """Calcula estimación de costo"""
        try:
            # Buscar archivo de presupuesto
            budget_files = [f for f in output_files if 'budget_estimate' in f]
            if budget_files:
                with open(budget_files[0], 'r') as f:
                    budget_data = json.load(f)
                    return budget_data.get('total_estimated_cost_usd', 0.0)
        except Exception:
            pass
        
        return 0.0
    
    def _calculate_timeline_estimate(self, design_data: SolutionDesignData, output_files: List[str]) -> str:
        """Calcula estimación de cronograma"""
        try:
            # Cronogramas base por tipo de solución
            base_timelines = {
                SolutionType.PTP: "2-3 semanas",
                SolutionType.PTMP: "4-6 semanas",
                SolutionType.WIFI: "3-4 semanas",
                SolutionType.FIBER: "6-8 semanas",
                SolutionType.HYBRID: "8-10 semanas",
                SolutionType.CLOUD: "2-4 semanas"
            }
            
            base_timeline = base_timelines.get(design_data.solution_type, "4-6 semanas")
            
            # Ajustar por complejidad
            complexity_factor = len(design_data.requirements) / 10
            if complexity_factor > 1.5:
                return f"{base_timeline} + 2-3 semanas adicionales"
            elif complexity_factor > 1.0:
                return f"{base_timeline} + 1-2 semanas adicionales"
            else:
                return base_timeline
                
        except Exception:
            return "4-6 semanas"
    
    def _calculate_quality_score(self, design_data: SolutionDesignData, output_files: List[str], errors: List[str]) -> float:
        """Calcula score de calidad del diseño"""
        
        base_score = 100.0
        
        # Penalizar por errores
        error_penalty = len(errors) * 10
        base_score -= error_penalty
        
        # Bonificar por archivos generados
        file_bonus = len(output_files) * 3
        base_score += file_bonus
        
        # Bonificar por tipo de solución (más complejo = más puntos)
        type_bonus = {
            SolutionType.PTP: 15,
            SolutionType.PTMP: 20,
            SolutionType.WIFI: 12,
            SolutionType.FIBER: 25,
            SolutionType.HYBRID: 30,
            SolutionType.CLOUD: 18
        }
        base_score += type_bonus.get(design_data.solution_type, 0)
        
        return max(0.0, min(100.0, base_score))
    
    def _update_stats(self, result: DesignResult, processing_time: float):
        """Actualiza estadísticas de rendimiento"""
        
        with threading.Lock():
            self.stats['designs_processed'] += 1
            self.stats['total_processing_time'] += processing_time
            
            # Calcular promedio
            if self.stats['designs_processed'] > 0:
                self.stats['average_processing_time'] = (
                    self.stats['total_processing_time'] / self.stats['designs_processed']
                )
            
            # Calcular tasa de éxito
            if result.success:
                self.stats['success_rate'] = (
                    (self.stats['success_rate'] * (self.stats['designs_processed'] - 1) + 1) / 
                    self.stats['designs_processed']
                )
            
            # Acumular costos estimados
            self.stats['total_cost_estimated'] += result.cost_estimate
    
    def _cache_result(self, design_id: str, result: DesignResult):
        """Guarda resultado en caché"""
        
        with self.cache_lock:
            self.result_cache[design_id] = result
            
            # Limpiar caché si es muy grande
            if len(self.result_cache) > 1000:
                oldest_keys = sorted(self.result_cache.keys())[:100]
                for key in oldest_keys:
                    del self.result_cache[key]
    
    def submit_design(self, design_data: SolutionDesignData) -> str:
        """Envía un diseño para procesamiento"""
        
        # Calcular prioridad real
        config = self.solution_configs[design_data.solution_type]
        priority_boost = config.get('priority_boost', 1.0)
        
        # Prioridad más baja = mayor prioridad en la cola
        real_priority = int(design_data.priority.value * priority_boost)
        
        # Agregar a la cola prioritaria
        self.job_queue.put((real_priority, design_data))
        
        logger.info(f"📋 Diseño {design_data.design_id} enviado con prioridad {real_priority}")
        
        return design_data.design_id
    
    def get_design_status(self, design_id: str) -> Optional[DesignResult]:
        """Obtiene el estado de un diseño"""
        
        # Verificar caché primero
        with self.cache_lock:
            if design_id in self.result_cache:
                return self.result_cache[design_id]
        
        # Si no está en caché, podría estar en procesamiento
        return None
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de rendimiento"""
        
        return self.stats.copy()
    
    def shutdown(self):
        """Apaga el procesador de diseño"""
        
        logger.info("🛑 Apagando procesador de Diseño de Solución...")
        
        # Enviar señal de parada a workers
        for _ in range(len(self.workers)):
            self.job_queue.put(None)
        
        # Esperar a que terminen
        for worker in self.workers:
            if hasattr(worker, 'join'):
                worker.join(timeout=5)
        
        # Cerrar pools
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)
        
        logger.info("✅ Procesador de Diseño de Solución apagado")

# Función para crear procesador de diseño
def create_solution_design_processor(max_workers: int = 24,
                                   enable_gpu: bool = False,
                                   enable_parallel: bool = True) -> SolutionDesignProcessor:
    """Crea una instancia del procesador de diseño"""
    
    try:
        processor = SolutionDesignProcessor(
            max_workers=max_workers,
            enable_gpu=enable_gpu,
            enable_parallel=enable_parallel
        )
        
        logger.info("✅ Procesador de Diseño de Solución creado exitosamente")
        return processor
        
    except Exception as e:
        logger.error(f"❌ Error creando procesador de diseño: {e}")
        return None

if __name__ == "__main__":
    # Probar procesador de diseño
    logger.info("🚀 Probando procesador de Diseño de Solución")
    
    processor = create_solution_design_processor()
    if processor:
        # Crear datos de prueba
        test_design = SolutionDesignData(
            design_id="DESIGN_001",
            solution_type=SolutionType.PTP,
            requirements={"bandwidth": "1 Gbps", "distance": "2 km", "reliability": "99.9%"},
            site_survey_data={"coordinates": [(19.4326, -99.1332), (19.4327, -99.1333)]},
            budget_constraints={"max_budget": 10000, "strict": False},
            timeline={"start_date": "2024-01-01", "end_date": "2024-02-01"},
            priority=DesignPriority.HIGH,
            timestamp=time.time()
        )
        
        # Enviar para procesamiento
        design_id = processor.submit_design(test_design)
        
        # Esperar un poco y verificar estado
        time.sleep(2)
        status = processor.get_design_status(design_id)
        
        if status:
            logger.info(f"✅ Diseño procesado: {status.success}")
            logger.info(f"📊 Tiempo de procesamiento: {status.processing_time:.2f}s")
            logger.info(f"🎯 Score de calidad: {status.quality_score:.1f}")
            logger.info(f"💰 Costo estimado: ${status.cost_estimate:,.2f}")
            logger.info(f"⏰ Cronograma estimado: {status.timeline_estimate}")
        else:
            logger.info("⏳ Diseño aún en procesamiento")
        
        # Mostrar estadísticas
        stats = processor.get_performance_stats()
        logger.info(f"📊 Estadísticas: {stats}")
        
        # Limpiar
        processor.shutdown()
    else:
        logger.error("❌ No se pudo crear el procesador de diseño") 