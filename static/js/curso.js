function validarFormulario() {
    // Obtener los valores de los campos del formulario
    const titulo = document.getElementById('id_titulo').value;
    const descripcion = document.getElementById('id_descripcion').value;
    const fechaInicio = document.getElementById('id_fecha_inicio').value;
    const fechaFin = document.getElementById('id_fecha_fin').value;

    // Inicializar un flag para verificar si el formulario es válido
    let esValido = true;

    // Limpiar los errores previos
    limpiarErrores();

    // Validación para el campo 'titulo'
    if (titulo === "") {
        mostrarError('id_titulo', 'El título es obligatorio.');
        esValido = false;
    }

    // Validación para el campo 'descripcion'
    if (descripcion === "") {
        mostrarError('id_descripcion', 'La descripción es obligatoria.');
        esValido = false;
    }

    // Validación para las fechas
    if (fechaInicio && fechaFin) {
    const inicio = new Date(fechaInicio);
    const fin = new Date(fechaFin);
    if (inicio >= fin) {
        mostrarError('id_fecha_fin', 'La fecha de fin debe ser posterior a la fecha de inicio.');
        esValido = false;
    }
}

    // Verificar si la fecha de inicio es mayor que la fecha de fin
    if (fechaInicio && fechaFin && new Date(fechaInicio) > new Date(fechaFin)) {
        mostrarError('id_fecha_fin', 'La fecha de fin no puede ser anterior a la fecha de inicio.');
        esValido = false;
    }

    return esValido;
}

// Función para mostrar errores
function mostrarError(campo, mensaje) {
    const errorDiv = document.getElementById(campo + 'Error');
    errorDiv.textContent = mensaje;
    document.getElementById(campo).classList.add('is-invalid');
}

// Función para limpiar los errores
function limpiarErrores() {
    const campos = ['id_titulo', 'id_descripcion', 'id_fecha_inicio', 'id_fecha_fin'];
    campos.forEach(campo => {
        document.getElementById(campo).classList.remove('is-invalid');
        document.getElementById(campo + 'Error').textContent = '';
    });
}

