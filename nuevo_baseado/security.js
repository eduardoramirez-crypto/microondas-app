// Módulo de seguridad avanzada para protección del código
// Este archivo contiene técnicas avanzadas de protección

class SecurityManager {
    constructor() {
        this.isDebugging = false;
        this.debugAttempts = 0;
        this.maxAttempts = 3;
        this.init();
    }

    init() {
        this.detectDevTools();
        this.preventRightClick();
        this.preventTextSelection();
        this.preventDragDrop();
        this.preventKeyboardShortcuts();
        this.detectConsoleAccess();
        this.obfuscateConsole();
        this.addIntegrityCheck();
    }

    // Detectar herramientas de desarrollador
    detectDevTools() {
        let devtools = { open: false, orientation: null };
        const threshold = 160;

        setInterval(() => {
            if (window.outerHeight - window.innerHeight > threshold || 
                window.outerWidth - window.innerWidth > threshold) {
                if (!devtools.open) {
                    devtools.open = true;
                    this.handleDevToolsDetection();
                }
            } else {
                devtools.open = false;
            }
        }, 500);

        // Detectar cambios en el tamaño de la ventana
        window.addEventListener('resize', () => {
            if (window.outerHeight - window.innerHeight > threshold || 
                window.outerWidth - window.innerWidth > threshold) {
                this.handleDevToolsDetection();
            }
        });
    }

    // Manejar detección de herramientas de desarrollador
    handleDevToolsDetection() {
        this.debugAttempts++;
        console.clear();
        
        if (this.debugAttempts <= this.maxAttempts) {
            console.log('%c⚠️ ACCESO NO AUTORIZADO DETECTADO ⚠️', 
                'color: red; font-size: 24px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);');
            console.log('%cLas herramientas de desarrollador están deshabilitadas para proteger la propiedad intelectual.', 
                'color: orange; font-size: 16px;');
            console.log('%cIntento ' + this.debugAttempts + ' de ' + this.maxAttempts, 
                'color: yellow; font-size: 14px;');
        } else {
            console.log('%c🚫 ACCESO BLOQUEADO 🚫', 
                'color: red; font-size: 28px; font-weight: bold;');
            console.log('%cSe ha detectado un intento de acceso no autorizado múltiples veces.', 
                'color: red; font-size: 16px;');
            // Opcional: redirigir o deshabilitar funcionalidad
            // this.disableApplication();
        }
    }

    // Prevenir clic derecho
    preventRightClick() {
        document.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            this.showWarning('Clic derecho deshabilitado');
            return false;
        });
    }

    // Prevenir selección de texto
    preventTextSelection() {
        document.addEventListener('selectstart', (e) => {
            e.preventDefault();
            return false;
        });

        document.addEventListener('dragstart', (e) => {
            e.preventDefault();
            return false;
        });

        // CSS para deshabilitar selección
        const style = document.createElement('style');
        style.textContent = `
            * {
                -webkit-user-select: none !important;
                -moz-user-select: none !important;
                -ms-user-select: none !important;
                user-select: none !important;
                -webkit-touch-callout: none !important;
                -webkit-tap-highlight-color: transparent !important;
            }
            
            input, textarea {
                -webkit-user-select: text !important;
                -moz-user-select: text !important;
                -ms-user-select: text !important;
                user-select: text !important;
            }
        `;
        document.head.appendChild(style);
    }

    // Prevenir arrastrar y soltar
    preventDragDrop() {
        document.addEventListener('dragover', (e) => e.preventDefault());
        document.addEventListener('drop', (e) => e.preventDefault());
    }

    // Prevenir atajos de teclado
    preventKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U
            if (e.key === 'F12' || 
                (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J')) ||
                (e.ctrlKey && e.key === 'U')) {
                e.preventDefault();
                this.showWarning('Atajo de teclado deshabilitado');
                return false;
            }
        });
    }

    // Detectar acceso a la consola
    detectConsoleAccess() {
        let devtools = false;
        const element = new Image();
        Object.defineProperty(element, 'id', {
            get: function() {
                devtools = true;
                console.clear();
                console.log('%c🔍 Acceso a la consola detectado', 'color: red; font-size: 18px;');
                throw new Error('Console access detected');
            }
        });
        
        setInterval(() => {
            devtools = false;
            console.log(element);
            console.clear();
            if (devtools) {
                this.handleDevToolsDetection();
            }
        }, 1000);
    }

    // Ofuscar la consola
    obfuscateConsole() {
        const originalConsole = window.console;
        const obfuscatedConsole = {
            log: () => {},
            warn: () => {},
            error: () => {},
            info: () => {},
            debug: () => {},
            trace: () => {},
            table: () => {},
            group: () => {},
            groupEnd: () => {},
            time: () => {},
            timeEnd: () => {},
            count: () => {},
            clear: () => {}
        };

        // Reemplazar console en producción
        if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
            window.console = obfuscatedConsole;
        }
    }

    // Verificación de integridad
    addIntegrityCheck() {
        const expectedChecksum = this.calculateChecksum();
        
        setInterval(() => {
            const currentChecksum = this.calculateChecksum();
            if (expectedChecksum !== currentChecksum) {
                console.error('Integridad del código comprometida');
                this.handleTampering();
            }
        }, 5000);
    }

    // Calcular checksum simple
    calculateChecksum() {
        const scripts = document.querySelectorAll('script');
        let checksum = 0;
        scripts.forEach(script => {
            if (script.textContent) {
                for (let i = 0; i < script.textContent.length; i++) {
                    checksum += script.textContent.charCodeAt(i);
                }
            }
        });
        return checksum;
    }

    // Manejar manipulación del código
    handleTampering() {
        console.clear();
        console.log('%c🚨 MANIPULACIÓN DETECTADA 🚨', 
            'color: red; font-size: 24px; font-weight: bold;');
        console.log('%cSe ha detectado una modificación no autorizada del código.', 
            'color: red; font-size: 16px;');
        
        // Opcional: deshabilitar funcionalidad crítica
        // this.disableApplication();
    }

    // Mostrar advertencia
    showWarning(message) {
        // Crear notificación temporal
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(239, 68, 68, 0.9);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-family: Arial, sans-serif;
            font-size: 14px;
            z-index: 10000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            animation: slideIn 0.3s ease-out;
        `;
        notification.textContent = message;
        
        // Agregar animación CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(notification);
        
        // Remover después de 3 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }

    // Deshabilitar aplicación (opcional)
    disableApplication() {
        document.body.innerHTML = `
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: #1a1a1a;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
            ">
                <div>
                    <h1 style="color: #ef4444; margin-bottom: 20px;">🚫 Acceso Denegado</h1>
                    <p>Se ha detectado un intento de acceso no autorizado.</p>
                    <p>Por favor, contacte al administrador del sistema.</p>
                </div>
            </div>
        `;
    }
}

// Inicializar protección cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new SecurityManager();
    });
} else {
    new SecurityManager();
}

// Exportar para uso en otros módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SecurityManager;
}
