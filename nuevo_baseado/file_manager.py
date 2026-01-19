import os
import json
import shutil
from datetime import datetime
from pathlib import Path
import hashlib

class FileManager:
    """Sistema de gestión de archivos generados y plantillas"""
    
    def __init__(self, base_dir="generated_files"):
        self.base_dir = Path(base_dir)
        self.templates_dir = self.base_dir / "templates"
        self.history_file = self.base_dir / "generation_history.json"
        self.settings_file = self.base_dir / "settings.json"
        
        # Crear directorios si no existen
        self.base_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        
        # Inicializar historial
        self.history = self.load_history()
        self.settings = self.load_settings()
    
    def load_history(self):
        """Carga el historial de generación"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            'files': [],
            'templates': [],
            'last_generation': None,
            'total_files': 0
        }
    
    def load_settings(self):
        """Carga la configuración del sistema"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            'auto_save': True,
            'backup_enabled': True,
            'max_history': 100,
            'default_template': None,
            'file_naming': 'timestamp',
            'compression_enabled': False
        }
    
    def save_history(self):
        """Guarda el historial de generación"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando historial: {e}")
            return False
    
    def save_settings(self):
        """Guarda la configuración del sistema"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando configuración: {e}")
            return False
    
    def save_generated_file(self, file_path, file_type, metadata=None, template_data=None):
        """Guarda un archivo generado en el sistema"""
        try:
            # Generar nombre único para el archivo guardado
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_hash = self.generate_file_hash(file_path)
            
            # Crear directorio por tipo de archivo
            type_dir = self.base_dir / file_type
            type_dir.mkdir(exist_ok=True)
            
            # Nombre del archivo guardado
            original_name = Path(file_path).stem
            extension = Path(file_path).suffix
            saved_name = f"{original_name}_{timestamp}{extension}"
            saved_path = type_dir / saved_name
            
            # Copiar archivo
            shutil.copy2(file_path, saved_path)
            
            # Crear entrada en el historial
            file_entry = {
                'id': file_hash,
                'original_path': str(file_path),
                'saved_path': str(saved_path),
                'file_type': file_type,
                'original_name': original_name,
                'saved_name': saved_name,
                'generation_date': timestamp,
                'file_size': os.path.getsize(saved_path),
                'metadata': metadata or {},
                'template_data': template_data or {}
            }
            
            # Agregar al historial
            self.history['files'].append(file_entry)
            self.history['last_generation'] = timestamp
            self.history['total_files'] += 1
            
            # Limpiar historial si excede el límite
            if len(self.history['files']) > self.settings['max_history']:
                self.history['files'] = self.history['files'][-self.settings['max_history']:]
            
            # Guardar historial
            self.save_history()
            
            return {
                'success': True,
                'saved_path': str(saved_path),
                'file_id': file_hash,
                'message': f'Archivo guardado como {saved_name}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Error guardando archivo'
            }
    
    def generate_file_hash(self, file_path):
        """Genera un hash único para el archivo"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except:
            return hashlib.md5(str(datetime.now()).encode()).hexdigest()
    
    def save_template(self, template_name, template_data, description=""):
        """Guarda una plantilla para reutilización"""
        try:
            template = {
                'name': template_name,
                'data': template_data,
                'description': description,
                'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'usage_count': 0,
                'last_used': None
            }
            
            # Guardar plantilla en archivo
            template_file = self.templates_dir / f"{template_name}.json"
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2, ensure_ascii=False)
            
            # Agregar al historial de plantillas
            self.history['templates'].append(template)
            self.save_history()
            
            return {
                'success': True,
                'template_name': template_name,
                'message': f'Plantilla {template_name} guardada'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Error guardando plantilla'
            }
    
    def load_template(self, template_name):
        """Carga una plantilla guardada"""
        try:
            template_file = self.templates_dir / f"{template_name}.json"
            if template_file.exists():
                with open(template_file, 'r', encoding='utf-8') as f:
                    template = json.load(f)
                
                # Actualizar estadísticas de uso
                template['usage_count'] += 1
                template['last_used'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Guardar plantilla actualizada
                with open(template_file, 'w', encoding='utf-8') as f:
                    json.dump(template, f, indent=2, ensure_ascii=False)
                
                return {
                    'success': True,
                    'template': template,
                    'message': f'Plantilla {template_name} cargada'
                }
            else:
                return {
                    'success': False,
                    'error': 'Plantilla no encontrada',
                    'message': f'La plantilla {template_name} no existe'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Error cargando plantilla'
            }
    
    def get_file_history(self, file_type=None, limit=None):
        """Obtiene el historial de archivos generados"""
        files = self.history['files']
        
        if file_type:
            files = [f for f in files if f['file_type'] == file_type]
        
        if limit:
            files = files[-limit:]
        
        return files
    
    def get_templates(self):
        """Obtiene la lista de plantillas disponibles"""
        return self.history['templates']
    
    def delete_file(self, file_id):
        """Elimina un archivo del historial"""
        try:
            # Encontrar archivo en el historial
            file_entry = None
            for i, file in enumerate(self.history['files']):
                if file['id'] == file_id:
                    file_entry = file
                    del self.history['files'][i]
                    break
            
            if file_entry:
                # Eliminar archivo físico
                if os.path.exists(file_entry['saved_path']):
                    os.remove(file_entry['saved_path'])
                
                # Actualizar contador
                self.history['total_files'] = max(0, self.history['total_files'] - 1)
                
                # Guardar historial
                self.save_history()
                
                return {
                    'success': True,
                    'message': f'Archivo {file_entry["saved_name"]} eliminado'
                }
            else:
                return {
                    'success': False,
                    'error': 'Archivo no encontrado',
                    'message': 'El archivo especificado no existe en el historial'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Error eliminando archivo'
            }
    
    def get_statistics(self):
        """Obtiene estadísticas del sistema"""
        total_size = sum(f['file_size'] for f in self.history['files'])
        
        stats = {
            'total_files': self.history['total_files'],
            'total_size': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'templates_count': len(self.history['templates']),
            'last_generation': self.history['last_generation'],
            'file_types': {}
        }
        
        # Contar archivos por tipo
        for file in self.history['files']:
            file_type = file['file_type']
            if file_type not in stats['file_types']:
                stats['file_types'][file_type] = 0
            stats['file_types'][file_type] += 1
        
        return stats
    
    def cleanup_old_files(self, days_old=30):
        """Limpia archivos antiguos"""
        try:
            cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            files_to_delete = []
            
            for file in self.history['files']:
                file_date = datetime.strptime(file['generation_date'], "%Y%m%d_%H%M%S").timestamp()
                if file_date < cutoff_date:
                    files_to_delete.append(file['id'])
            
            deleted_count = 0
            for file_id in files_to_delete:
                result = self.delete_file(file_id)
                if result['success']:
                    deleted_count += 1
            
            return {
                'success': True,
                'deleted_count': deleted_count,
                'message': f'{deleted_count} archivos antiguos eliminados'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Error limpiando archivos antiguos'
            }

# Instancia global del gestor de archivos
file_manager = FileManager() 