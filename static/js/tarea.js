// Obtener referencias a los elementos del formulario
const form = document.querySelector('form');
const tituloInput = document.getElementById('id_titulo');
const descripcionInput = document.getElementById('id_descripcion');
const fechaLimiteInput = document.getElementById('id_fecha_limite');
const estadoSelect = document.getElementById('id_estado');

// Función principal de validación
function validarFormulario() {
    let esValido = true;

    // Validar título
    if (!tituloInput.value.trim()) {
        mostrarError(tituloInput, 'El título es obligatorio');
        esValido = false;
    } else if (tituloInput.value.length > 200) {
        mostrarError(tituloInput, 'El título no puede exceder los 200 caracteres');
        esValido = false;
    } else {
        quitarError(tituloInput);
    }

    // Validar descripción
    if (!descripcionInput.value.trim()) {
        mostrarError(descripcionInput, 'La descripción es obligatoria');
        esValido = false;
    } else if (descripcionInput.value.length > 1000) {
        mostrarError(descripcionInput, 'La descripción no puede exceder los 1000 caracteres');
        esValido = false;
    } else {
        quitarError(descripcionInput);
    }

    // Validar fecha límite
    if (!fechaLimiteInput.value) {
        mostrarError(fechaLimiteInput, 'La fecha de entrega es obligatoria');
        esValido = false;
    } else {
        const fechaActual = new Date();
        fechaActual.setHours(0, 0, 0, 0);
        const fechaLimite = new Date(fechaLimiteInput.value);

        if (fechaLimite < fechaActual) {
            mostrarError(fechaLimiteInput, 'La fecha de entrega no puede ser anterior a la fecha actual');
            esValido = false;
        } else {
            quitarError(fechaLimiteInput);
        }
    }

    // Validar estado
    if (!estadoSelect.value) {
        mostrarError(estadoSelect, 'El estado es obligatorio');
        esValido = false;
    } else {
        quitarError(estadoSelect);
    }

    return esValido;
}

// Validaciones en tiempo real
tituloInput.addEventListener('input', function() {
    if (!this.value.trim()) {
        mostrarError(this, 'El título es obligatorio');
    } else if (this.value.length > 200) {
        mostrarError(this, 'El título no puede exceder los 200 caracteres');
    } else {
        quitarError(this);
    }
});

descripcionInput.addEventListener('input', function() {
    if (!this.value.trim()) {
        mostrarError(this, 'La descripción es obligatoria');
    } else if (this.value.length > 1000) {
        mostrarError(this, 'La descripción no puede exceder los 1000 caracteres');
    } else {
        quitarError(this);
    }
});

fechaLimiteInput.addEventListener('change', function() {
    if (!this.value) {
        mostrarError(this, 'La fecha de entrega es obligatoria');
    } else {
        const fechaActual = new Date();
        fechaActual.setHours(0, 0, 0, 0);
        const fechaLimite = new Date(this.value);

        if (fechaLimite < fechaActual) {
            mostrarError(this, 'La fecha de entrega no puede ser anterior o la misma que la fecha actual');
        } else {
            quitarError(this);
        }
    }
});

estadoSelect.addEventListener('change', function() {
    if (!this.value) {
        mostrarError(this, 'El estado es obligatorio');
    } else {
        quitarError(this);
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

// Contador de caracteres para título y descripción
function agregarContadorCaracteres() {
    const contenedorTitulo = tituloInput.parentElement;
    const contenedorDescripcion = descripcionInput.parentElement;

    const contadorTitulo = document.createElement('small');
    contadorTitulo.className = 'text-muted';
    contenedorTitulo.appendChild(contadorTitulo);

    const contadorDescripcion = document.createElement('small');
    contadorDescripcion.className = 'text-muted';
    contenedorDescripcion.appendChild(contadorDescripcion);

    function actualizarContador(input, contador, max) {
        const actual = input.value.length;
        contador.textContent = `${actual}/${max} caracteres`;
        contador.style.color = actual > max ? 'red' : '#6c757d';
    }

    tituloInput.addEventListener('input', () => actualizarContador(tituloInput, contadorTitulo, 200));
    descripcionInput.addEventListener('input', () => actualizarContador(descripcionInput, contadorDescripcion, 1000));

    // Inicializar contadores
    actualizarContador(tituloInput, contadorTitulo, 200);
    actualizarContador(descripcionInput, contadorDescripcion, 1000);
}

// Inicializar contadores al cargar la página
document.addEventListener('DOMContentLoaded', agregarContadorCaracteres);