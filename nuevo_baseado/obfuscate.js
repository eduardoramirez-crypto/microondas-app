// Script de ofuscación para proteger el código JavaScript
// Este script debe ejecutarse antes de desplegar en producción

const fs = require('fs');
const path = require('path');

// Función para ofuscar código JavaScript básico
function obfuscateCode(code) {
    // Reemplazar nombres de variables comunes con nombres aleatorios
    const variableMap = new Map();
    let counter = 0;
    
    // Generar nombres aleatorios
    function generateRandomName() {
        const chars = 'abcdefghijklmnopqrstuvwxyz';
        let result = '';
        for (let i = 0; i < 3 + Math.floor(Math.random() * 3); i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result + counter++;
    }
    
    // Ofuscar nombres de variables y funciones
    code = code.replace(/\b(function|var|let|const)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/g, (match, keyword, name) => {
        if (!variableMap.has(name)) {
            variableMap.set(name, generateRandomName());
        }
        return `${keyword} ${variableMap.get(name)}`;
    });
    
    // Remover comentarios
    code = code.replace(/\/\*[\s\S]*?\*\//g, '');
    code = code.replace(/\/\/.*$/gm, '');
    
    // Remover espacios innecesarios
    code = code.replace(/\s+/g, ' ');
    code = code.replace(/;\s*/g, ';');
    
    return code;
}

// Función para agregar técnicas anti-debugging
function addAntiDebugging(code) {
    const antiDebugCode = `
    // Anti-debugging techniques
    (function() {
        let devtools = {open: false, orientation: null};
        const threshold = 160;
        
        setInterval(function() {
            if (window.outerHeight - window.innerHeight > threshold || 
                window.outerWidth - window.innerWidth > threshold) {
                if (!devtools.open) {
                    devtools.open = true;
                    console.clear();
                    console.log('%c¡Acceso no autorizado detectado!', 'color: red; font-size: 20px;');
                    // Opcional: redirigir o mostrar mensaje
                    // window.location.href = 'about:blank';
                }
            } else {
                devtools.open = false;
            }
        }, 500);
        
        // Detectar F12
        document.addEventListener('keydown', function(e) {
            if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I')) {
                e.preventDefault();
                console.clear();
                console.log('%c¡Herramientas de desarrollador deshabilitadas!', 'color: red; font-size: 16px;');
                return false;
            }
        });
        
        // Detectar clic derecho
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            return false;
        });
        
        // Detectar selección de texto
        document.addEventListener('selectstart', function(e) {
            e.preventDefault();
            return false;
        });
        
        // Detectar arrastrar
        document.addEventListener('dragstart', function(e) {
            e.preventDefault();
            return false;
        });
    })();
    `;
    
    return antiDebugCode + code;
}

// Función para minificar CSS
function minifyCSS(css) {
    return css
        .replace(/\/\*[\s\S]*?\*\//g, '') // Remover comentarios
        .replace(/\s+/g, ' ') // Remover espacios múltiples
        .replace(/;\s*/g, ';') // Remover espacios después de punto y coma
        .replace(/{\s*/g, '{') // Remover espacios después de {
        .replace(/}\s*/g, '}') // Remover espacios después de }
        .replace(/:\s*/g, ':') // Remover espacios después de :
        .replace(/,\s*/g, ',') // Remover espacios después de ,
        .trim();
}

// Función principal
function protectCode() {
    console.log('🛡️ Iniciando protección de código...');
    
    // Leer el archivo HTML
    const htmlPath = path.join(__dirname, 'templates', 'ptpFangioactualizacion.html');
    let htmlContent = fs.readFileSync(htmlPath, 'utf8');
    
    // Extraer y ofuscar JavaScript inline
    const scriptRegex = /<script[^>]*>([\s\S]*?)<\/script>/gi;
    htmlContent = htmlContent.replace(scriptRegex, (match, scriptContent) => {
        if (scriptContent.trim()) {
            const obfuscatedScript = obfuscateCode(scriptContent);
            const protectedScript = addAntiDebugging(obfuscatedScript);
            return match.replace(scriptContent, protectedScript);
        }
        return match;
    });
    
    // Minificar CSS inline
    const styleRegex = /<style[^>]*>([\s\S]*?)<\/style>/gi;
    htmlContent = htmlContent.replace(styleRegex, (match, styleContent) => {
        if (styleContent.trim()) {
            const minifiedCSS = minifyCSS(styleContent);
            return match.replace(styleContent, minifiedCSS);
        }
        return match;
    });
    
    // Crear versión protegida
    const protectedPath = path.join(__dirname, 'templates', 'ptpFangioactualizacion_protected.html');
    fs.writeFileSync(protectedPath, htmlContent);
    
    console.log('✅ Código protegido guardado en:', protectedPath);
    console.log('📊 Estadísticas:');
    console.log('   - Tamaño original:', (fs.statSync(htmlPath).size / 1024).toFixed(2), 'KB');
    console.log('   - Tamaño protegido:', (fs.statSync(protectedPath).size / 1024).toFixed(2), 'KB');
}

// Ejecutar si se llama directamente
if (require.main === module) {
    protectCode();
}

module.exports = { obfuscateCode, addAntiDebugging, minifyCSS, protectCode };
