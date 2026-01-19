// FUNCIÓN PARA GUARDAR ARCHIVO DE DISEÑO DE SOLUCIÓN
function guardarArchivoDiseno(user_id, tipoDocumento, filaIdx) {
    console.log('Guardando archivo de diseño para:', user_id, tipoDocumento, filaIdx);
    
    // Mostrar inmediatamente el modal para nuevo ID (como en Site Survey)
    mostrarModalNuevoId();
}

// FUNCIÓN PARA PREGUNTAR SI QUIERE GENERAR OTRO ARCHIVO
function preguntarGenerarOtro() {
    const respuesta = confirm('¿Quieres generar otro archivo de diseño de solución?\n\n' +
                            'Si seleccionas "Aceptar", podrás ingresar un nuevo ID para generar otro archivo.');
    
    if (respuesta) {
        // Mostrar modal para nuevo ID
        mostrarModalNuevoId();
    }
}

// FUNCIÓN PARA MOSTRAR MODAL DE NUEVO ID
function mostrarModalNuevoId() {
    // Crear el modal si no existe
    if (!document.getElementById('modalNuevoId')) {
        const modalHTML = `
            <div id="modalNuevoId" class="modal-overlay">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2><i class="fas fa-plus-circle"></i> Generar Nuevo Archivo</h2>
                        <button onclick="cerrarModalNuevoId()" class="modal-close">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    
                    <div class="modal-body">
                        <p>Ingresa el ID del nuevo sitio para generar otro archivo:</p>
                        
                        <div class="input-group">
                            <i class="fas fa-id-card"></i>
                            <input type="text" id="nuevoIdInput" placeholder="Ej: 5140066159E" 
                                   class="nuevo-id-input" maxlength="20">
                        </div>
                        
                        <div class="modal-actions">
                            <button onclick="generarArchivoNuevoId()" class="btn-generar">
                                <i class="fas fa-play"></i> Generar Archivo
                            </button>
                            <button onclick="cerrarModalNuevoId()" class="btn-cancelar">
                                <i class="fas fa-times"></i> Cancelar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }
    
    // Mostrar el modal
    document.getElementById('modalNuevoId').style.display = 'flex';
    
    // Enfocar el input y agregar evento Enter
    const input = document.getElementById('nuevoIdInput');
    input.focus();
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            generarArchivoNuevoId();
        }
    });
}

// FUNCIÓN PARA CERRAR MODAL DE NUEVO ID
function cerrarModalNuevoId() {
    const modal = document.getElementById('modalNuevoId');
    if (modal) {
        modal.style.display = 'none';
    }
}

// FUNCIÓN PARA GENERAR ARCHIVO CON NUEVO ID
function generarArchivoNuevoId() {
    const nuevoId = document.getElementById('nuevoIdInput').value.trim();
    if (!nuevoId) {
        alert('⚠️ Por favor, ingresa un ID válido');
        return;
    }
    
    // Cerrar modal
    cerrarModalNuevoId();
    
    // Mostrar indicador de carga
    mostrarIndicadorCarga();
    
    // Llamar a la API para generar el DISEÑO DE SOLUCIÓN del nuevo ID
    fetch('/generar_diseno_solucion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_id: nuevoId,
            fila_idx: '0'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
                    // Éxito - redirigir al diseño de solución generado CON LLENADO AUTOMÁTICO
        window.location.href = `/diseno_solucion_directo?user_id=${nuevoId}&fila_idx=0&llenado_automatico=true`;
        } else {
            // Error
            alert('❌ Error al generar diseño de solución: ' + (data.message || 'Error desconocido'));
            ocultarIndicadorCarga();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('❌ Error de conexión. Verifica tu internet e intenta de nuevo.');
        ocultarIndicadorCarga();
    });
}

// FUNCIÓN PARA MOSTRAR INDICADOR DE CARGA
function mostrarIndicadorCarga() {
    // Crear overlay de carga si no existe
    if (!document.getElementById('overlayCarga')) {
        const overlayHTML = `
            <div id="overlayCarga" class="overlay-carga">
                <div class="carga-content">
                    <div class="spinner"></div>
                    <h3>Generando Diseño de Solución...</h3>
                    <p>Procesando ID: ${document.getElementById('nuevoIdInput').value}</p>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', overlayHTML);
    }
    document.getElementById('overlayCarga').style.display = 'flex';
}

// FUNCIÓN PARA OCULTAR INDICADOR DE CARGA
function ocultarIndicadorCarga() {
    const overlay = document.getElementById('overlayCarga');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

console.log('✅ JavaScript de Diseño de Solución cargado correctamente');
