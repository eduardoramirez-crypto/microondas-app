#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Compresión Extrema para Fangio Telecom
Máxima velocidad con compresión inteligente
"""

import os
import time
import logging
import hashlib
import json
import gzip
import bz2
import lzma
import zlib
from typing import Dict, List, Tuple, Optional, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from dataclasses import dataclass
from enum import Enum
import numpy as np
from PIL import Image
import io

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fangio_compression.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CompressionLevel(Enum):
    """Niveles de compresión"""
    ULTRA_FAST = 'ultra_fast'      # Máxima velocidad, mínima compresión
    FAST = 'fast'                   # Velocidad alta, compresión media
    BALANCED = 'balanced'           # Equilibrio velocidad/compresión
    HIGH = 'high'                   # Alta compresión, menor velocidad
    MAXIMUM = 'maximum'             # Máxima compresión, menor velocidad

class CompressionAlgorithm(Enum):
    """Algoritmos de compresión"""
    GZIP = 'gzip'
    BZIP2 = 'bzip2'
    LZMA = 'lzma'
    ZLIB = 'zlib'
    LZ4 = 'lz4'
    ZSTD = 'zstd'
    CUSTOM = 'custom'

@dataclass
class CompressionResult:
    """Resultado de compresión"""
    original_size: int
    compressed_size: int
    compression_ratio: float
    compression_time: float
    algorithm: str
    quality_score: float
    output_path: str

class ExtremeCompressor:
    """Compresor extremo para máxima velocidad"""
    
    def __init__(self, 
                 max_workers: int = 16,
                 enable_gpu: bool = False,
                 enable_parallel: bool = True):
        
        self.max_workers = max_workers
        self.enable_gpu = enable_gpu
        self.enable_parallel = enable_parallel
        
        # Configuración de algoritmos
        self.algorithms = {
            CompressionAlgorithm.GZIP: {
                'compresslevel': 1,  # Máxima velocidad
                'timeout': 0.1
            },
            CompressionAlgorithm.BZIP2: {
                'compresslevel': 1,  # Máxima velocidad
                'timeout': 0.2
            },
            CompressionAlgorithm.LZMA: {
                'preset': 0,  # Máxima velocidad
                'timeout': 0.3
            },
            CompressionAlgorithm.ZLIB: {
                'level': 1,  # Máxima velocidad
                'timeout': 0.05
            }
        }
        
        # Thread pool para compresión paralela
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        
        # Caché de compresión
        self.compression_cache = {}
        self.cache_lock = threading.Lock()
        
        # Estadísticas
        self.stats = {
            'files_compressed': 0,
            'total_original_size': 0,
            'total_compressed_size': 0,
            'total_compression_time': 0,
            'average_compression_ratio': 0,
            'peak_throughput': 0
        }
        
        logger.info(f"🚀 Compresor extremo iniciado con {max_workers} workers")
    
    def compress_file(self, 
                     file_path: str, 
                     output_path: str = None,
                     algorithm: CompressionAlgorithm = CompressionAlgorithm.GZIP,
                     level: CompressionLevel = CompressionLevel.ULTRA_FAST) -> CompressionResult:
        """Comprime un archivo individual"""
        
        start_time = time.time()
        
        try:
            # Verificar caché
            cache_key = self._generate_cache_key(file_path, algorithm, level)
            cached_result = self._get_from_cache(cache_key)
            
            if cached_result:
                logger.info(f"📋 Compresión obtenida de caché para {file_path}")
                return cached_result
            
            # Obtener tamaño original
            original_size = os.path.getsize(file_path)
            
            # Determinar algoritmo óptimo
            optimal_algorithm = self._select_optimal_algorithm(file_path, level)
            
            # Comprimir archivo
            compressed_size, output_path = self._compress_with_algorithm(
                file_path, output_path, optimal_algorithm, level
            )
            
            # Calcular métricas
            compression_time = time.time() - start_time
            compression_ratio = (1 - compressed_size / original_size) * 100
            quality_score = self._calculate_quality_score(compression_ratio, compression_time)
            
            # Crear resultado
            result = CompressionResult(
                original_size=original_size,
                compressed_size=compressed_size,
                compression_ratio=compression_ratio,
                compression_time=compression_time,
                algorithm=optimal_algorithm.value,
                quality_score=quality_score,
                output_path=output_path
            )
            
            # Guardar en caché
            self._save_to_cache(cache_key, result)
            
            # Actualizar estadísticas
            self._update_stats(result)
            
            logger.info(f"✅ Archivo comprimido: {file_path} -> {compression_ratio:.1f}% en {compression_time:.3f}s")
            
            return result
            
        except Exception as e:
            compression_time = time.time() - start_time
            logger.error(f"❌ Error comprimiendo {file_path}: {e}")
            
            return CompressionResult(
                original_size=0,
                compressed_size=0,
                compression_ratio=0,
                compression_time=compression_time,
                algorithm='none',
                quality_score=0,
                output_path=''
            )
    
    def _select_optimal_algorithm(self, file_path: str, level: CompressionLevel) -> CompressionAlgorithm:
        """Selecciona el algoritmo óptimo según el archivo y nivel"""
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # Para imágenes, usar compresión especializada
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return CompressionAlgorithm.CUSTOM
        
        # Para texto, usar algoritmos rápidos
        if file_extension in ['.txt', '.csv', '.json', '.xml', '.html']:
            if level == CompressionLevel.ULTRA_FAST:
                return CompressionAlgorithm.ZLIB
            elif level == CompressionLevel.FAST:
                return CompressionAlgorithm.GZIP
            else:
                return CompressionAlgorithm.BZIP2
        
        # Para archivos binarios, usar LZMA para mejor compresión
        if level in [CompressionLevel.HIGH, CompressionLevel.MAXIMUM]:
            return CompressionAlgorithm.LZMA
        else:
            return CompressionAlgorithm.GZIP
    
    def _compress_with_algorithm(self, 
                                file_path: str, 
                                output_path: str,
                                algorithm: CompressionAlgorithm,
                                level: CompressionLevel) -> Tuple[int, str]:
        """Comprime un archivo con el algoritmo especificado"""
        
        if output_path is None:
            output_path = self._generate_output_path(file_path, algorithm)
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if algorithm == CompressionAlgorithm.CUSTOM:
            return self._compress_image(file_path, output_path, level)
        elif algorithm == CompressionAlgorithm.GZIP:
            return self._compress_gzip(file_path, output_path, level)
        elif algorithm == CompressionAlgorithm.BZIP2:
            return self._compress_bzip2(file_path, output_path, level)
        elif algorithm == CompressionAlgorithm.LZMA:
            return self._compress_lzma(file_path, output_path, level)
        elif algorithm == CompressionAlgorithm.ZLIB:
            return self._compress_zlib(file_path, output_path, level)
        else:
            # Fallback a gzip
            return self._compress_gzip(file_path, output_path, level)
    
    def _compress_image(self, image_path: str, output_path: str, level: CompressionLevel) -> Tuple[int, str]:
        """Compresión especializada para imágenes"""
        
        try:
            with Image.open(image_path) as img:
                # Configuración según nivel
                if level == CompressionLevel.ULTRA_FAST:
                    quality = 30
                    optimize = False
                    progressive = False
                elif level == CompressionLevel.FAST:
                    quality = 50
                    optimize = True
                    progressive = False
                elif level == CompressionLevel.BALANCED:
                    quality = 70
                    optimize = True
                    progressive = True
                else:
                    quality = 85
                    optimize = True
                    progressive = True
                
                # Redimensionar si es muy grande
                if level in [CompressionLevel.ULTRA_FAST, CompressionLevel.FAST]:
                    if img.size[0] > 1280 or img.size[1] > 720:
                        img.thumbnail((1280, 720), Image.Resampling.LANCZOS)
                
                # Guardar comprimida
                img.save(output_path, 'JPEG', quality=quality, optimize=optimize, progressive=progressive)
                
                compressed_size = os.path.getsize(output_path)
                return compressed_size, output_path
                
        except Exception as e:
            logger.error(f"❌ Error comprimiendo imagen {image_path}: {e}")
            # Fallback a copia simple
            import shutil
            shutil.copy2(image_path, output_path)
            return os.path.getsize(output_path), output_path
    
    def _compress_gzip(self, file_path: str, output_path: str, level: CompressionLevel) -> Tuple[int, str]:
        """Compresión con GZIP"""
        
        compress_level = 1 if level == CompressionLevel.ULTRA_FAST else 6
        
        with open(file_path, 'rb') as f_in:
            with gzip.open(output_path, 'wb', compresslevel=compress_level) as f_out:
                f_out.writelines(f_in)
        
        return os.path.getsize(output_path), output_path
    
    def _compress_bzip2(self, file_path: str, output_path: str, level: CompressionLevel) -> Tuple[int, str]:
        """Compresión con BZIP2"""
        
        compress_level = 1 if level == CompressionLevel.ULTRA_FAST else 9
        
        with open(file_path, 'rb') as f_in:
            with bz2.open(output_path, 'wb', compresslevel=compress_level) as f_out:
                f_out.writelines(f_in)
        
        return os.path.getsize(output_path), output_path
    
    def _compress_lzma(self, file_path: str, output_path: str, level: CompressionLevel) -> Tuple[int, str]:
        """Compresión con LZMA"""
        
        preset = 0 if level == CompressionLevel.ULTRA_FAST else 6
        
        with open(file_path, 'rb') as f_in:
            with lzma.open(output_path, 'wb', preset=preset) as f_out:
                f_out.writelines(f_in)
        
        return os.path.getsize(output_path), output_path
    
    def _compress_zlib(self, file_path: str, output_path: str, level: CompressionLevel) -> Tuple[int, str]:
        """Compresión con ZLIB"""
        
        compress_level = 1 if level == CompressionLevel.ULTRA_FAST else 9
        
        with open(file_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                compressor = zlib.compressobj(compress_level)
                while True:
                    chunk = f_in.read(8192)
                    if not chunk:
                        break
                    compressed_chunk = compressor.compress(chunk)
                    if compressed_chunk:
                        f_out.write(compressed_chunk)
                
                # Finalizar compresión
                final_chunk = compressor.flush()
                if final_chunk:
                    f_out.write(final_chunk)
        
        return os.path.getsize(output_path), output_path
    
    def _generate_output_path(self, file_path: str, algorithm: CompressionAlgorithm) -> str:
        """Genera ruta de salida para archivo comprimido"""
        
        base_name = os.path.splitext(file_path)[0]
        
        if algorithm == CompressionAlgorithm.CUSTOM:
            extension = '.jpg'
        elif algorithm == CompressionAlgorithm.GZIP:
            extension = '.gz'
        elif algorithm == CompressionAlgorithm.BZIP2:
            extension = '.bz2'
        elif algorithm == CompressionAlgorithm.LZMA:
            extension = '.xz'
        elif algorithm == CompressionAlgorithm.ZLIB:
            extension = '.zlib'
        else:
            extension = '.compressed'
        
        output_path = f"{base_name}_compressed{extension}"
        
        # Si ya existe, agregar número
        counter = 1
        while os.path.exists(output_path):
            output_path = f"{base_name}_compressed_{counter}{extension}"
            counter += 1
        
        return output_path
    
    def _calculate_quality_score(self, compression_ratio: float, compression_time: float) -> float:
        """Calcula score de calidad de la compresión"""
        
        # Score basado en compresión (0-70 puntos)
        compression_score = min(compression_ratio / 2, 70)
        
        # Score basado en velocidad (0-30 puntos)
        speed_score = max(0, 30 - (compression_time * 100))
        
        return compression_score + speed_score
    
    def _update_stats(self, result: CompressionResult):
        """Actualiza estadísticas de compresión"""
        
        with threading.Lock():
            self.stats['files_compressed'] += 1
            self.stats['total_original_size'] += result.original_size
            self.stats['total_compressed_size'] += result.compressed_size
            self.stats['total_compression_time'] += result.compression_time
            
            # Calcular promedio de compresión
            if self.stats['files_compressed'] > 0:
                self.stats['average_compression_ratio'] = (
                    (1 - self.stats['total_compressed_size'] / self.stats['total_original_size']) * 100
                )
            
            # Calcular throughput pico
            current_throughput = result.original_size / result.compression_time if result.compression_time > 0 else 0
            if current_throughput > self.stats['peak_throughput']:
                self.stats['peak_throughput'] = current_throughput
    
    def batch_compress(self, 
                      file_paths: List[str],
                      level: CompressionLevel = CompressionLevel.ULTRA_FAST,
                      algorithm: CompressionAlgorithm = None) -> List[CompressionResult]:
        """Comprime múltiples archivos en paralelo"""
        
        logger.info(f"🚀 Iniciando compresión por lotes de {len(file_paths)} archivos")
        
        results = []
        
        if self.enable_parallel:
            # Compresión paralela
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_path = {
                    executor.submit(
                        self.compress_file,
                        path,
                        None,
                        algorithm or self._select_optimal_algorithm(path, level),
                        level
                    ): path
                    for path in file_paths
                }
                
                for future in as_completed(future_to_path):
                    path = future_to_path[future]
                    try:
                        result = future.result()
                        results.append(result)
                        
                        if result.compression_ratio > 0:
                            logger.info(f"✅ {path}: {result.compression_ratio:.1f}% compresión")
                        
                    except Exception as e:
                        logger.error(f"❌ Error comprimiendo {path}: {e}")
        else:
            # Compresión secuencial
            for file_path in file_paths:
                try:
                    result = self.compress_file(
                        file_path,
                        algorithm=algorithm or self._select_optimal_algorithm(file_path, level),
                        level=level
                    )
                    results.append(result)
                except Exception as e:
                    logger.error(f"❌ Error comprimiendo {file_path}: {e}")
        
        # Resumen del lote
        successful_results = [r for r in results if r.compression_ratio > 0]
        if successful_results:
            avg_compression = sum(r.compression_ratio for r in successful_results) / len(successful_results)
            total_saved = sum(r.original_size - r.compressed_size for r in successful_results)
            total_time = sum(r.compression_time for r in successful_results)
            
            logger.info(f"📊 Lote completado: {len(successful_results)}/{len(file_paths)} exitosas")
            logger.info(f"📊 Compresión promedio: {avg_compression:.1f}%")
            logger.info(f"📊 Espacio ahorrado: {total_saved / (1024*1024):.1f} MB")
            logger.info(f"📊 Tiempo total: {total_time:.1f}s")
        
        return results
    
    def _generate_cache_key(self, file_path: str, algorithm: CompressionAlgorithm, level: CompressionLevel) -> str:
        """Genera clave única para el caché"""
        
        key_data = {
            'path': file_path,
            'algorithm': algorithm.value,
            'level': level.value,
            'file_mtime': os.path.getmtime(file_path) if os.path.exists(file_path) else 0
        }
        
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[CompressionResult]:
        """Obtiene resultado del caché"""
        
        with self.cache_lock:
            return self.compression_cache.get(cache_key)
    
    def _save_to_cache(self, cache_key: str, result: CompressionResult):
        """Guarda resultado en el caché"""
        
        with self.cache_lock:
            # Limpiar caché si es muy grande
            if len(self.compression_cache) > 1000:
                # Eliminar entradas más antiguas
                oldest_keys = sorted(self.compression_cache.keys())[:100]
                for key in oldest_keys:
                    del self.compression_cache[key]
            
            self.compression_cache[cache_key] = result
    
    def clear_cache(self):
        """Limpia el caché de compresión"""
        
        with self.cache_lock:
            self.compression_cache.clear()
            logger.info("🧹 Caché de compresión limpiado")
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas de compresión"""
        
        return self.stats.copy()
    
    def export_stats(self, file_path: str = None) -> str:
        """Exporta estadísticas a un archivo"""
        
        try:
            if file_path is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                file_path = f"fangio_compression_stats_{timestamp}.json"
            
            stats = self.get_stats()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, default=str)
            
            logger.info(f"📁 Estadísticas exportadas a {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"❌ Error exportando estadísticas: {e}")
            return ""

# Función para crear compresor extremo
def create_extreme_compressor(max_workers: int = 16,
                             enable_gpu: bool = False,
                             enable_parallel: bool = True) -> ExtremeCompressor:
    """Crea una instancia del compresor extremo"""
    
    try:
        compressor = ExtremeCompressor(
            max_workers=max_workers,
            enable_gpu=enable_gpu,
            enable_parallel=enable_parallel
        )
        
        logger.info("✅ Compresor extremo creado exitosamente")
        return compressor
        
    except Exception as e:
        logger.error(f"❌ Error creando compresor extremo: {e}")
        return None

# Función para compresión simple
def compress_single_file(file_path: str,
                        output_path: str = None,
                        level: str = 'ultra_fast') -> Dict:
    """Función simple para comprimir un archivo"""
    
    try:
        compressor = create_extreme_compressor()
        if not compressor:
            return {'success': False, 'error': 'No se pudo crear el compresor'}
        
        # Convertir nivel
        compression_level = CompressionLevel(level)
        
        # Comprimir archivo
        result = compressor.compress_file(file_path, output_path, level=compression_level)
        
        return {
            'success': True,
            'original_size': result.original_size,
            'compressed_size': result.compressed_size,
            'compression_ratio': result.compression_ratio,
            'compression_time': result.compression_time,
            'algorithm': result.algorithm,
            'quality_score': result.quality_score,
            'output_path': result.output_path
        }
        
    except Exception as e:
        logger.error(f"❌ Error comprimiendo archivo {file_path}: {e}")
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    # Crear y probar el compresor extremo
    logger.info("🚀 Probando compresor extremo")
    
    compressor = create_extreme_compressor()
    if compressor:
        # Crear archivo de prueba
        test_file = "test_compression.txt"
        with open(test_file, 'w') as f:
            f.write("Este es un archivo de prueba para compresión extrema. " * 1000)
        
        try:
            # Comprimir archivo
            result = compressor.compress_file(test_file, level=CompressionLevel.ULTRA_FAST)
            
            if result.compression_ratio > 0:
                logger.info("✅ Prueba de compresión exitosa")
                logger.info(f"📊 Compresión: {result.compression_ratio:.1f}%")
                logger.info(f"⏱️ Tiempo: {result.compression_time:.3f}s")
                logger.info(f"🎯 Score: {result.quality_score:.1f}/100")
            else:
                logger.error("❌ Prueba de compresión falló")
        
        finally:
            # Limpiar archivo de prueba
            try:
                os.remove(test_file)
                if os.path.exists(result.output_path):
                    os.remove(result.output_path)
            except:
                pass
        
        # Mostrar estadísticas
        stats = compressor.get_stats()
        logger.info(f"📊 Estadísticas: {stats}")
        
        # Limpiar
        compressor.clear_cache()
    else:
        logger.error("❌ No se pudo crear el compresor extremo") 