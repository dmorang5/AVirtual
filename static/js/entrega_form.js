// Constantes para validación de archivos
const TIPOS_PERMITIDOS = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'text/plain',
    'image/jpeg',
    'image/png'
];
const TAMANO_MAXIMO = 5 * 1024 * 1024; // 5MB en bytes

// Obtener referencias a los elementos del formulario
const form = document.querySelector('form');
const archivoInput = document.getElementById('archivo');

function validarEntregaTarea() {
    let esValido = true;

    // Validar si se seleccionó un archivo
    if (!archivoInput.files || !archivoInput.files[0]) {
        mostrarError(archivoInput, 'Debe seleccionar un archivo');
        esValido = false;
    } else {
        const archivo = archivoInput.files[0];

        // Validar tipo de archivo
        if (!TIPOS_PERMITIDOS.includes(archivo.type)) {
            mostrarError(archivoInput, 'Tipo de archivo no permitido. Solo se permiten archivos PDF, Word, Excel, PowerPoint, TXT, JPG y PNG');
            esValido = false;
        }

        // Validar tamaño del archivo
        if (archivo.size > TAMANO_MAXIMO) {
            mostrarError(archivoInput, 'El archivo no puede superar los 5MB');
            esValido = false;
        }
    }

    // Validar si la fecha actual es posterior a la fecha límite
    const fechaLimite = new Date(document.getElementById('fecha_limite').value);
    const fechaActual = new Date();

    if (fechaActual > fechaLimite) {
        mostrarError(archivoInput, 'La fecha límite de entrega ha expirado');
        esValido = false;
    }

    if (esValido) {
        // Mostrar indicador de carga
        mostrarCargando();
    }

    return esValido;
}

// Validación en tiempo real del archivo
archivoInput.addEventListener('change', function() {
    if (!this.files || !this.files[0]) {
        mostrarError(this, 'Debe seleccionar un archivo');
        return;
    }

    const archivo = this.files[0];

    // Validar tipo de archivo
    if (!TIPOS_PERMITIDOS.includes(archivo.type)) {
        mostrarError(this, 'Tipo de archivo no permitido. Solo se permiten archivos PDF, Word, Excel, PowerPoint, TXT, JPG y PNG');
        return;
    }

    // Validar tamaño del archivo
    if (archivo.size > TAMANO_MAXIMO) {
        mostrarError(this, 'El archivo no puede superar los 5MB');
        return;
    }

    // Si todo está bien, quitar el error
    quitarError(this);
});

function mostrarError(input, mensaje) {
    const errorDiv = document.getElementById('archivoError');
    input.classList.add('is-invalid');
    errorDiv.textContent = mensaje;
    errorDiv.style.display = 'block';
}

function quitarError(input) {
    const errorDiv = document.getElementById('archivoError');
    input.classList.remove('is-invalid');
    errorDiv.style.display = 'none';
}

function mostrarCargando() {
    const submitBtn = document.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Subiendo...';
}

// Agregar información visual sobre tipos de archivos permitidos
document.addEventListener('DOMContentLoaded', function() {
    const archivoContainer = archivoInput.parentElement;
    const infoText = document.createElement('small');
    infoText.className = 'text-muted d-block mt-1';
    infoText.innerHTML = 'Formatos permitidos: PDF, Word, TXT<br>Tamaño máximo: 5MB';
    archivoContainer.appendChild(infoText);
});