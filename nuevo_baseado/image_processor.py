#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador Optimizado de Imágenes para Fangio Telecom
Compresión, redimensionamiento y optimización de imágenes
"""

import os
import time
import logging
import hashlib
from typing import Dict, List, Tuple, Optional, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import io
import json
from functools import lru_cache
import threading
from dataclasses import dataclass
from enum import Enum

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fangio_images.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ImageFormat(Enum):
    """Formatos de imagen soportados"""
    JPEG = 'JPEG'
    PNG = 'PNG'
    WEBP = 'WEBP'
    GIF = 'GIF'

class CompressionLevel(Enum):
    """Niveles de compresión"""
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    ULTRA = 'ultra'

@dataclass
class ImageMetadata:
    """Metadatos de una imagen"""
    file_path: str
    file_name: str
    file_size: int
    dimensions: Tuple[int, int]
    format: str
    mode: str
    dpi: Tuple[int, int]
    created_time: float
    modified_time: float

@dataclass
class ProcessingResult:
    """Resultado del procesamiento de imagen"""
    success: bool
    original_size: int
    processed_size: int
    compression_ratio: float
    processing_time: float
    output_path: str
    quality_score: float
    error_message: Optional[str] = None

class ImageProcessor:
    """Procesador optimizado de imágenes"""
    
    def __init__(self, 
                 max_workers: int = 4,
                 default_quality: int = 85,
                 max_dimensions: Tuple[int, int] = (1920, 1080),
                 enable_webp: bool = True,
                 enable_progressive: bool = True):
        
        self.max_workers = max_workers
        self.default_quality = default_quality
        self.max_dimensions = max_dimensions
        self.enable_webp = enable_webp
        self.enable_progressive = enable_progressive
        
        # Caché de procesamiento
        self.processing_cache = {}
        self.cache_lock = threading.Lock()
        
        # Estadísticas
        self.stats = {
            'images_processed': 0,
            'total_compression_saved': 0,
            'total_processing_time': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        
        # Configuración de formatos
        self.format_configs = {
            ImageFormat.JPEG: {
                'quality': 85,
                'optimize': True,
                'progressive': True,
                'subsampling': 0
            },
            ImageFormat.PNG: {
                'optimize': True,
                'compress_level': 6
            },
            ImageFormat.WEBP: {
                'quality': 85,
                'method': 6,
                'lossless': False
            }
        }
        
        logger.info(f"🚀 Procesador de imágenes inicializado con {max_workers} workers")
    
    def process_image(self, 
                     input_path: str, 
                     output_path: str = None,
                     format: ImageFormat = ImageFormat.JPEG,
                     quality: int = None,
                     resize: bool = True,
                     enhance: bool = True) -> ProcessingResult:
        """Procesa una imagen individual"""
        
        start_time = time.time()
        
        try:
            # Verificar caché
            cache_key = self._generate_cache_key(input_path, format, quality, resize, enhance)
            cached_result = self._get_from_cache(cache_key)
            
            if cached_result:
                self.stats['cache_hits'] += 1
                logger.info(f"📋 Resultado obtenido de caché para {input_path}")
                return cached_result
            
            self.stats['cache_misses'] += 1
            
            # Cargar imagen
            with Image.open(input_path) as img:
                # Obtener metadatos originales
                original_size = os.path.getsize(input_path)
                original_dimensions = img.size
                
                # Procesar imagen
                processed_img = self._process_image_internal(
                    img, resize, enhance, format
                )
                
                # Determinar calidad
                if quality is None:
                    quality = self.format_configs[format].get('quality', self.default_quality)
                
                # Guardar imagen procesada
                if output_path is None:
                    output_path = self._generate_output_path(input_path, format)
                
                self._save_image(processed_img, output_path, format, quality)
                
                # Calcular resultados
                processed_size = os.path.getsize(output_path)
                compression_ratio = (1 - processed_size / original_size) * 100
                processing_time = time.time() - start_time
                
                # Calcular calidad
                quality_score = self._calculate_quality_score(
                    original_dimensions, processed_img.size, compression_ratio
                )
                
                # Crear resultado
                result = ProcessingResult(
                    success=True,
                    original_size=original_size,
                    processed_size=processed_size,
                    compression_ratio=compression_ratio,
                    processing_time=processing_time,
                    output_path=output_path,
                    quality_score=quality_score
                )
                
                # Guardar en caché
                self._save_to_cache(cache_key, result)
                
                # Actualizar estadísticas
                self.stats['images_processed'] += 1
                self.stats['total_compression_saved'] += (original_size - processed_size)
                self.stats['total_processing_time'] += processing_time
                
                logger.info(f"✅ Imagen procesada: {input_path} -> {output_path}")
                logger.info(f"📊 Compresión: {compression_ratio:.1f}% | Tiempo: {processing_time:.2f}s")
                
                return result
                
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"❌ Error procesando imagen {input_path}: {e}")
            
            return ProcessingResult(
                success=False,
                original_size=0,
                processed_size=0,
                compression_ratio=0,
                processing_time=processing_time,
                output_path="",
                quality_score=0,
                error_message=str(e)
            )
    
    def _process_image_internal(self, 
                               img: Image.Image, 
                               resize: bool, 
                               enhance: bool, 
                               format: ImageFormat) -> Image.Image:
        """Procesa la imagen internamente"""
        
        # Convertir formato si es necesario
        if format == ImageFormat.JPEG and img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        elif format == ImageFormat.PNG and img.mode == 'RGB':
            img = img.convert('RGBA')
        
        # Redimensionar si es necesario
        if resize and (img.size[0] > self.max_dimensions[0] or img.size[1] > self.max_dimensions[1]):
            img = self._resize_image(img, self.max_dimensions)
        
        # Mejorar calidad si está habilitado
        if enhance:
            img = self._enhance_image(img)
        
        return img
    
    def _resize_image(self, img: Image.Image, max_dimensions: Tuple[int, int]) -> Image.Image:
        """Redimensiona la imagen manteniendo proporción"""
        try:
            # Calcular nuevas dimensiones
            ratio = min(max_dimensions[0] / img.size[0], max_dimensions[1] / img.size[1])
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            
            # Redimensionar con algoritmo de alta calidad
            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            logger.debug(f"🔄 Imagen redimensionada: {img.size} -> {new_size}")
            return resized_img
            
        except Exception as e:
            logger.error(f"❌ Error redimensionando imagen: {e}")
            return img
    
    def _enhance_image(self, img: Image.Image) -> Image.Image:
        """Mejora la calidad de la imagen"""
        try:
            # Aplicar filtros de mejora
            enhanced_img = img
            
            # Mejorar nitidez
            enhanced_img = enhanced_img.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
            
            # Mejorar contraste
            enhancer = ImageEnhance.Contrast(enhanced_img)
            enhanced_img = enhancer.enhance(1.1)
            
            # Mejorar saturación (solo para imágenes RGB)
            if enhanced_img.mode == 'RGB':
                enhancer = ImageEnhance.Color(enhanced_img)
                enhanced_img = enhancer.enhance(1.05)
            
            logger.debug("✨ Imagen mejorada con filtros de calidad")
            return enhanced_img
            
        except Exception as e:
            logger.error(f"❌ Error mejorando imagen: {e}")
            return img
    
    def _save_image(self, 
                    img: Image.Image, 
                    output_path: str, 
                    format: ImageFormat, 
                    quality: int):
        """Guarda la imagen en el formato especificado"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Configuración del formato
            save_kwargs = self.format_configs[format].copy()
            
            # Aplicar calidad específica
            if 'quality' in save_kwargs:
                save_kwargs['quality'] = quality
            
            # Guardar imagen
            img.save(output_path, format.value, **save_kwargs)
            
            logger.debug(f"💾 Imagen guardada: {output_path}")
            
        except Exception as e:
            logger.error(f"❌ Error guardando imagen: {e}")
            raise
    
    def _generate_output_path(self, input_path: str, format: ImageFormat) -> str:
        """Genera ruta de salida para la imagen procesada"""
        base_name = os.path.splitext(input_path)[0]
        extension = format.value.lower()
        
        # Agregar sufijo de procesamiento
        output_path = f"{base_name}_processed.{extension}"
        
        # Si ya existe, agregar número
        counter = 1
        while os.path.exists(output_path):
            output_path = f"{base_name}_processed_{counter}.{extension}"
            counter += 1
        
        return output_path
    
    def _calculate_quality_score(self, 
                                original_dimensions: Tuple[int, int], 
                                processed_dimensions: Tuple[int, int], 
                                compression_ratio: float) -> float:
        """Calcula un score de calidad de la imagen procesada"""
        try:
            # Score basado en resolución mantenida
            resolution_score = min(processed_dimensions[0] / original_dimensions[0], 
                                 processed_dimensions[1] / original_dimensions[1])
            
            # Score basado en compresión (mejor compresión = mejor score)
            compression_score = min(compression_ratio / 50, 1.0)  # Máximo 50% de compresión
            
            # Score combinado
            quality_score = (resolution_score * 0.7 + compression_score * 0.3) * 100
            
            return max(0, min(100, quality_score))  # Limitar entre 0 y 100
            
        except Exception as e:
            logger.error(f"❌ Error calculando score de calidad: {e}")
            return 50.0  # Score por defecto
    
    def batch_process(self, 
                     image_paths: List[str], 
                     output_dir: str = None,
                     format: ImageFormat = ImageFormat.JPEG,
                     quality: int = None,
                     resize: bool = True,
                     enhance: bool = True) -> List[ProcessingResult]:
        """Procesa múltiples imágenes en paralelo"""
        
        logger.info(f"🚀 Iniciando procesamiento por lotes de {len(image_paths)} imágenes")
        
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Crear tareas
            future_to_path = {
                executor.submit(
                    self.process_image,
                    path,
                    self._get_batch_output_path(path, output_dir, format) if output_dir else None,
                    format,
                    quality,
                    resize,
                    enhance
                ): path
                for path in image_paths
            }
            
            # Procesar resultados
            for future in as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result.success:
                        logger.info(f"✅ {path}: {result.compression_ratio:.1f}% compresión")
                    else:
                        logger.error(f"❌ {path}: {result.error_message}")
                        
                except Exception as e:
                    logger.error(f"❌ Error procesando {path}: {e}")
                    results.append(ProcessingResult(
                        success=False,
                        original_size=0,
                        processed_size=0,
                        compression_ratio=0,
                        processing_time=0,
                        output_path="",
                        quality_score=0,
                        error_message=str(e)
                    ))
        
        # Resumen del procesamiento
        successful_results = [r for r in results if r.success]
        if successful_results:
            avg_compression = sum(r.compression_ratio for r in successful_results) / len(successful_results)
            total_saved = sum(r.original_size - r.processed_size for r in successful_results)
            total_time = sum(r.processing_time for r in successful_results)
            
            logger.info(f"📊 Lote completado: {len(successful_results)}/{len(image_paths)} exitosas")
            logger.info(f"📊 Compresión promedio: {avg_compression:.1f}%")
            logger.info(f"📊 Espacio ahorrado: {total_saved / (1024*1024):.1f} MB")
            logger.info(f"📊 Tiempo total: {total_time:.1f}s")
        
        return results
    
    def _get_batch_output_path(self, input_path: str, output_dir: str, format: ImageFormat) -> str:
        """Genera ruta de salida para procesamiento por lotes"""
        file_name = os.path.basename(input_path)
        base_name = os.path.splitext(file_name)[0]
        extension = format.value.lower()
        
        output_path = os.path.join(output_dir, f"{base_name}_processed.{extension}")
        
        # Si ya existe, agregar número
        counter = 1
        while os.path.exists(output_path):
            output_path = os.path.join(output_dir, f"{base_name}_processed_{counter}.{extension}")
            counter += 1
        
        return output_path
    
    def get_image_metadata(self, image_path: str) -> Optional[ImageMetadata]:
        """Obtiene metadatos de una imagen"""
        try:
            if not os.path.exists(image_path):
                return None
            
            with Image.open(image_path) as img:
                stat = os.stat(image_path)
                
                metadata = ImageMetadata(
                    file_path=image_path,
                    file_name=os.path.basename(image_path),
                    file_size=stat.st_size,
                    dimensions=img.size,
                    format=img.format,
                    mode=img.mode,
                    dpi=img.info.get('dpi', (72, 72)),
                    created_time=stat.st_ctime,
                    modified_time=stat.st_mtime
                )
                
                return metadata
                
        except Exception as e:
            logger.error(f"❌ Error obteniendo metadatos de {image_path}: {e}")
            return None
    
    def batch_get_metadata(self, image_paths: List[str]) -> List[Optional[ImageMetadata]]:
        """Obtiene metadatos de múltiples imágenes en paralelo"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_path = {
                executor.submit(self.get_image_metadata, path): path
                for path in image_paths
            }
            
            for future in as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    metadata = future.result()
                    results.append(metadata)
                except Exception as e:
                    logger.error(f"❌ Error obteniendo metadatos de {path}: {e}")
                    results.append(None)
        
        return results
    
    def _generate_cache_key(self, 
                           input_path: str, 
                           format: ImageFormat, 
                           quality: int, 
                           resize: bool, 
                           enhance: bool) -> str:
        """Genera clave única para el caché"""
        key_data = {
            'path': input_path,
            'format': format.value,
            'quality': quality,
            'resize': resize,
            'enhance': enhance,
            'file_mtime': os.path.getmtime(input_path) if os.path.exists(input_path) else 0
        }
        
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[ProcessingResult]:
        """Obtiene resultado del caché"""
        with self.cache_lock:
            return self.processing_cache.get(cache_key)
    
    def _save_to_cache(self, cache_key: str, result: ProcessingResult):
        """Guarda resultado en el caché"""
        with self.cache_lock:
            # Limpiar caché si es muy grande
            if len(self.processing_cache) > 1000:
                # Eliminar entradas más antiguas
                oldest_keys = sorted(self.processing_cache.keys())[:100]
                for key in oldest_keys:
                    del self.processing_cache[key]
            
            self.processing_cache[cache_key] = result
    
    def clear_cache(self):
        """Limpia el caché de procesamiento"""
        with self.cache_lock:
            self.processing_cache.clear()
            logger.info("🧹 Caché de procesamiento limpiado")
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del procesador"""
        avg_processing_time = (self.stats['total_processing_time'] / self.stats['images_processed'] 
                              if self.stats['images_processed'] > 0 else 0)
        
        cache_hit_rate = (self.stats['cache_hits'] / 
                         (self.stats['cache_hits'] + self.stats['cache_misses']) * 100
                         if (self.stats['cache_hits'] + self.stats['cache_misses']) > 0 else 0)
        
        return {
            'images_processed': self.stats['images_processed'],
            'total_compression_saved_mb': self.stats['total_compression_saved'] / (1024*1024),
            'total_processing_time': self.stats['total_processing_time'],
            'average_processing_time': avg_processing_time,
            'cache_hits': self.stats['cache_hits'],
            'cache_misses': self.stats['cache_misses'],
            'cache_hit_rate': cache_hit_rate,
            'cache_size': len(self.processing_cache)
        }
    
    def export_stats(self, file_path: str = None) -> str:
        """Exporta estadísticas a un archivo"""
        try:
            if file_path is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                file_path = f"fangio_image_stats_{timestamp}.json"
            
            stats = self.get_stats()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, default=str)
            
            logger.info(f"📁 Estadísticas exportadas a {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"❌ Error exportando estadísticas: {e}")
            return ""

class ImageBatchProcessor:
    """Procesador de lotes de imágenes con interfaz simplificada"""
    
    def __init__(self, processor: ImageProcessor):
        self.processor = processor
        self.batch_history = []
    
    def process_directory(self, 
                         input_dir: str, 
                         output_dir: str = None,
                         format: ImageFormat = ImageFormat.JPEG,
                         quality: int = None,
                         resize: bool = True,
                         enhance: bool = True,
                         file_patterns: List[str] = None) -> Dict:
        """Procesa todas las imágenes en un directorio"""
        
        try:
            # Obtener lista de archivos de imagen
            image_files = self._get_image_files(input_dir, file_patterns)
            
            if not image_files:
                logger.warning(f"⚠️ No se encontraron imágenes en {input_dir}")
                return {'success': False, 'message': 'No se encontraron imágenes'}
            
            # Crear directorio de salida si no existe
            if output_dir is None:
                output_dir = os.path.join(input_dir, 'processed')
            
            os.makedirs(output_dir, exist_ok=True)
            
            # Procesar imágenes
            start_time = time.time()
            results = self.processor.batch_process(
                image_files, output_dir, format, quality, resize, enhance
            )
            total_time = time.time() - start_time
            
            # Crear resumen
            summary = self._create_batch_summary(results, total_time, input_dir, output_dir)
            
            # Guardar en historial
            self.batch_history.append(summary)
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Error procesando directorio {input_dir}: {e}")
            return {'success': False, 'error': str(e)}
    
    def _get_image_files(self, directory: str, patterns: List[str] = None) -> List[str]:
        """Obtiene lista de archivos de imagen en un directorio"""
        if patterns is None:
            patterns = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff']
        
        image_files = []
        
        for pattern in patterns:
            import glob
            files = glob.glob(os.path.join(directory, pattern))
            image_files.extend(files)
        
        # Eliminar duplicados y ordenar
        image_files = sorted(list(set(image_files)))
        
        return image_files
    
    def _create_batch_summary(self, 
                             results: List[ProcessingResult], 
                             total_time: float,
                             input_dir: str,
                             output_dir: str) -> Dict:
        """Crea un resumen del procesamiento por lotes"""
        
        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]
        
        total_original_size = sum(r.original_size for r in successful_results)
        total_processed_size = sum(r.processed_size for r in successful_results)
        total_saved = total_original_size - total_processed_size
        
        avg_compression = (sum(r.compression_ratio for r in successful_results) / len(successful_results) 
                          if successful_results else 0)
        
        summary = {
            'success': True,
            'timestamp': time.time(),
            'input_directory': input_dir,
            'output_directory': output_dir,
            'total_images': len(results),
            'successful_images': len(successful_results),
            'failed_images': len(failed_results),
            'total_original_size_mb': total_original_size / (1024*1024),
            'total_processed_size_mb': total_processed_size / (1024*1024),
            'total_saved_mb': total_saved / (1024*1024),
            'average_compression': avg_compression,
            'total_processing_time': total_time,
            'success_rate': len(successful_results) / len(results) * 100 if results else 0
        }
        
        return summary
    
    def get_batch_history(self) -> List[Dict]:
        """Obtiene historial de procesamiento por lotes"""
        return self.batch_history.copy()
    
    def clear_history(self):
        """Limpia el historial de procesamiento"""
        self.batch_history.clear()
        logger.info("🧹 Historial de procesamiento limpiado")

# Función para crear instancia del procesador
def create_image_processor(max_workers: int = 4, 
                          default_quality: int = 85,
                          max_dimensions: Tuple[int, int] = (1920, 1080)) -> ImageProcessor:
    """Crea una instancia del procesador de imágenes"""
    try:
        processor = ImageProcessor(
            max_workers=max_workers,
            default_quality=default_quality,
            max_dimensions=max_dimensions
        )
        
        logger.info("✅ Procesador de imágenes creado exitosamente")
        return processor
        
    except Exception as e:
        logger.error(f"❌ Error creando procesador de imágenes: {e}")
        return None

# Función para procesar imagen simple
def process_single_image(input_path: str, 
                        output_path: str = None,
                        format: str = 'JPEG',
                        quality: int = 85,
                        resize: bool = True) -> Dict:
    """Función simple para procesar una imagen"""
    try:
        processor = create_image_processor()
        if not processor:
            return {'success': False, 'error': 'No se pudo crear el procesador'}
        
        # Convertir formato
        image_format = ImageFormat(format.upper())
        
        # Procesar imagen
        result = processor.process_image(
            input_path, output_path, image_format, quality, resize, True
        )
        
        return {
            'success': result.success,
            'original_size': result.original_size,
            'processed_size': result.processed_size,
            'compression_ratio': result.compression_ratio,
            'processing_time': result.processing_time,
            'output_path': result.output_path,
            'quality_score': result.quality_score,
            'error_message': result.error_message
        }
        
    except Exception as e:
        logger.error(f"❌ Error procesando imagen {input_path}: {e}")
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    # Crear y probar el procesador
    logger.info("🚀 Iniciando procesador de imágenes")
    
    processor = create_image_processor()
    if processor:
        # Probar procesamiento simple
        test_image = "test_image.jpg"  # Crear una imagen de prueba
        
        if os.path.exists(test_image):
            result = processor.process_image(test_image)
            if result.success:
                logger.info("✅ Prueba de procesamiento exitosa")
                logger.info(f"📊 Compresión: {result.compression_ratio:.1f}%")
                logger.info(f"⏱️ Tiempo: {result.processing_time:.2f}s")
            else:
                logger.error(f"❌ Prueba falló: {result.error_message}")
        else:
            logger.info("ℹ️ No hay imagen de prueba, creando una...")
            # Crear imagen de prueba simple
            test_img = Image.new('RGB', (800, 600), color='blue')
            test_img.save(test_image)
            
            # Procesar
            result = processor.process_image(test_image)
            if result.success:
                logger.info("✅ Prueba con imagen creada exitosa")
        
        # Mostrar estadísticas
        stats = processor.get_stats()
        logger.info(f"📊 Estadísticas: {stats}")
        
        # Limpiar
        processor.clear_cache()
    else:
        logger.error("❌ No se pudo crear el procesador de imágenes") 