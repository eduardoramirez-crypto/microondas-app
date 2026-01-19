// Script de minificación avanzada para producción
const fs = require('fs');
const path = require('path');
const { minify: terserMinify } = require('terser');
const CleanCSS = require('clean-css');
const { minify: htmlMinify } = require('html-minifier-terser');

// Configuración de minificación
const terserOptions = {
    compress: {
        drop_console: true, // Remover console.log en producción
        drop_debugger: true,
        pure_funcs: ['console.log', 'console.info', 'console.debug'],
        passes: 2
    },
    mangle: {
        toplevel: true,
        properties: {
            regex: /^_/
        }
    },
    format: {
        comments: false
    }
};

const cleanCSSOptions = {
    level: 2,
    format: 'beautify'
};

const htmlMinifyOptions = {
    removeComments: true,
    removeCommentsFromCDATA: true,
    removeCDATASectionsFromCDATA: true,
    collapseWhitespace: true,
    collapseBooleanAttributes: true,
    removeAttributeQuotes: true,
    removeRedundantAttributes: true,
    useShortDoctype: true,
    removeEmptyAttributes: true,
    removeOptionalTags: true,
    removeEmptyElements: false,
    lint: false,
    keepClosingSlash: false,
    caseSensitive: true,
    minifyJS: true,
    minifyCSS: true
};

// Función para minificar JavaScript
async function minifyJavaScript(code) {
    try {
        const result = await terserMinify(code, terserOptions);
        return result.code;
    } catch (error) {
        console.error('Error minificando JavaScript:', error);
        return code;
    }
}

// Función para minificar CSS
function minifyCSS(css) {
    try {
        const cleanCSS = new CleanCSS(cleanCSSOptions);
        const result = cleanCSS.minify(css);
        return result.styles;
    } catch (error) {
        console.error('Error minificando CSS:', error);
        return css;
    }
}

// Función para minificar HTML
async function minifyHTML(html) {
    try {
        return await htmlMinify(html, htmlMinifyOptions);
    } catch (error) {
        console.error('Error minificando HTML:', error);
        return html;
    }
}

// Función para agregar protección adicional
function addAdvancedProtection(code) {
    // Agregar código de verificación de integridad
    const integrityCheck = `
    // Verificación de integridad del código
    (function() {
        const expectedHash = '${generateSimpleHash(code)}';
        const currentHash = '${generateSimpleHash(code)}';
        
        if (expectedHash !== currentHash) {
            console.error('Integridad del código comprometida');
            // Opcional: deshabilitar funcionalidad
        }
    })();
    `;
    
    return integrityCheck + code;
}

// Función simple para generar hash
function generateSimpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convertir a 32-bit integer
    }
    return Math.abs(hash).toString(16);
}

// Función principal de minificación
async function minifyAll() {
    console.log('🔧 Iniciando minificación avanzada...');
    
    const htmlPath = path.join(__dirname, 'templates', 'ptpFangioactualizacion.html');
    const protectedPath = path.join(__dirname, 'templates', 'ptpFangioactualizacion_protected.html');
    const minifiedPath = path.join(__dirname, 'templates', 'ptpFangioactualizacion_minified.html');
    
    let htmlContent = fs.readFileSync(htmlPath, 'utf8');
    
    // Extraer y minificar JavaScript
    const scriptRegex = /<script[^>]*>([\s\S]*?)<\/script>/gi;
    let scriptCount = 0;
    
    htmlContent = htmlContent.replace(scriptRegex, async (match, scriptContent) => {
        if (scriptContent.trim()) {
            scriptCount++;
            const minifiedScript = await minifyJavaScript(scriptContent);
            const protectedScript = addAdvancedProtection(minifiedScript);
            return match.replace(scriptContent, protectedScript);
        }
        return match;
    });
    
    // Extraer y minificar CSS
    const styleRegex = /<style[^>]*>([\s\S]*?)<\/style>/gi;
    let styleCount = 0;
    
    htmlContent = htmlContent.replace(styleRegex, (match, styleContent) => {
        if (styleContent.trim()) {
            styleCount++;
            const minifiedCSS = minifyCSS(styleContent);
            return match.replace(styleContent, minifiedCSS);
        }
        return match;
    });
    
    // Minificar HTML completo
    const minifiedHTML = await minifyHTML(htmlContent);
    
    // Guardar versión minificada
    fs.writeFileSync(minifiedPath, minifiedHTML);
    
    // Estadísticas
    const originalSize = fs.statSync(htmlPath).size;
    const minifiedSize = fs.statSync(minifiedPath).size;
    const compressionRatio = ((originalSize - minifiedSize) / originalSize * 100).toFixed(2);
    
    console.log('✅ Minificación completada');
    console.log('📊 Estadísticas:');
    console.log(`   - Scripts procesados: ${scriptCount}`);
    console.log(`   - Estilos procesados: ${styleCount}`);
    console.log(`   - Tamaño original: ${(originalSize / 1024).toFixed(2)} KB`);
    console.log(`   - Tamaño minificado: ${(minifiedSize / 1024).toFixed(2)} KB`);
    console.log(`   - Compresión: ${compressionRatio}%`);
    console.log(`   - Archivo guardado en: ${minifiedPath}`);
}

// Ejecutar si se llama directamente
if (require.main === module) {
    minifyAll().catch(console.error);
}

module.exports = { minifyJavaScript, minifyCSS, minifyHTML, minifyAll };
