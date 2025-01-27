// Obtener referencias a los elementos del formulario
const form = document.querySelector('form');
const tituloInput = document.getElementById('id_titulo');
const descripcionInput = document.getElementById('id_descripcion');
const fechaInicioInput = document.getElementById('id_fecha_inicio');
const fechaFinInput = document.getElementById('id_fecha_fin');

// Función principal de validación
function validarFormulario() {
    let esValido = true;
    
    // Validar título
    if (!tituloInput.value.trim()) {
        mostrarError(tituloInput, 'El título es obligatorio');
        esValido = false;
    } else if (tituloInput.value.length > 100) {
        mostrarError(tituloInput, 'El título no puede exceder los 100 caracteres');
        esValido = false;
    } else {
        quitarError(tituloInput);
    }

    // Validar descripción
    if (!descripcionInput.value.trim()) {
        mostrarError(descripcionInput, 'La descripción es obligatoria');
        esValido = false;
    } else {
        quitarError(descripcionInput);
    }

    // Validar fecha de inicio
    if (!fechaInicioInput.value) {
        mostrarError(fechaInicioInput, 'La fecha de inicio es obligatoria');
        esValido = false;
    } else {
        quitarError(fechaInicioInput);
    }

    // Validar fecha de fin
    if (!fechaFinInput.value) {
        mostrarError(fechaFinInput, 'La fecha de fin es obligatoria');
        esValido = false;
    } else {
        const fechaInicio = new Date(fechaInicioInput.value);
        const fechaFin = new Date(fechaFinInput.value);
        
        if (fechaFin < fechaInicio) {
            mostrarError(fechaFinInput, 'La fecha de fin no puede ser anterior a la fecha de inicio');
            esValido = false;
        } else {
            quitarError(fechaFinInput);
        }
    }

    return esValido;
}

// Validación en tiempo real
tituloInput.addEventListener('input', function() {
    if (!this.value.trim()) {
        mostrarError(this, 'El título es obligatorio');
    } else if (this.value.length > 100) {
        mostrarError(this, 'El título no puede exceder los 100 caracteres');
    } else {
        quitarError(this);
    }
});

descripcionInput.addEventListener('input', function() {
    if (!this.value.trim()) {
        mostrarError(this, 'La descripción es obligatoria');
    } else {
        quitarError(this);
    }
});

fechaInicioInput.addEventListener('change', function() {
    if (!this.value) {
        mostrarError(this, 'La fecha de inicio es obligatoria');
    } else {
        quitarError(this);
        // Validar fecha fin si ya tiene un valor
        if (fechaFinInput.value) {
            const fechaInicio = new Date(this.value);
            const fechaFin = new Date(fechaFinInput.value);
            
            if (fechaFin < fechaInicio) {
                mostrarError(fechaFinInput, 'La fecha de fin no puede ser anterior a la fecha de inicio');
            } else {
                quitarError(fechaFinInput);
            }
        }
    }
});

fechaFinInput.addEventListener('change', function() {
    if (!this.value) {
        mostrarError(this, 'La fecha de fin es obligatoria');
    } else if (fechaInicioInput.value) {
        const fechaInicio = new Date(fechaInicioInput.value);
        const fechaFin = new Date(this.value);
        
        if (fechaFin < fechaInicio) {
            mostrarError(this, 'La fecha de fin no puede ser anterior a la fecha de inicio');
        } else {
            quitarError(this);
        }
    }
});

// Funciones auxiliares
function mostrarError(input, mensaje) {
    const errorDiv = document.getElementById(input.id + 'Error');
    input.classList.add('is-invalid');
    errorDiv.textContent = mensaje;
}

function quitarError(input) {
    const errorDiv = document.getElementById(input.id + 'Error');
    input.classList.remove('is-invalid');
    errorDiv.textContent = '';
}