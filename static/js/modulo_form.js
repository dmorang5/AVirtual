document.addEventListener('DOMContentLoaded', function () {
    // Obtener referencias a los elementos del formulario
    const form = document.querySelector('form');
    const tituloInput = document.getElementById('id_titulo');
    const descripcionInput = document.getElementById('id_descripcion');
    const ordenInput = document.getElementById('id_orden');

    // Asegúrate de que las referencias a los elementos no sean nulas
    if (tituloInput && descripcionInput && ordenInput) {
        // Validación en tiempo real para el título
        tituloInput.addEventListener('input', function () {
            if (!this.value.trim()) {
                mostrarError(this, 'El título es obligatorio');
            } else if (this.value.length > 100) {
                mostrarError(this, 'El título no puede tener más de 100 caracteres');
            } else {
                quitarError(this);
            }
        });

        // Validación en tiempo real para la descripción
        descripcionInput.addEventListener('input', function () {
            if (!this.value.trim()) {
                mostrarError(this, 'La descripción es obligatoria');
            } else {
                quitarError(this);
            }
        });

        // Validación en tiempo real para el orden
        ordenInput.addEventListener('input', function () {
            if (!this.value) {
                mostrarError(this, 'El orden es obligatorio');
            } else if (parseInt(this.value) < 1) {
                mostrarError(this, 'El orden debe ser un número positivo');
            } else {
                quitarError(this);
            }
        });

        // Validación al enviar el formulario
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            let esValido = true;

            // Validar título
            if (!tituloInput.value.trim()) {
                mostrarError(tituloInput, 'El título es obligatorio');
                esValido = false;
            } else if (tituloInput.value.length > 100) {
                mostrarError(tituloInput, 'El título no puede tener más de 100 caracteres');
                esValido = false;
            }

            // Validar descripción
            if (!descripcionInput.value.trim()) {
                mostrarError(descripcionInput, 'La descripción es obligatoria');
                esValido = false;
            }

            // Validar orden
            if (!ordenInput.value) {
                mostrarError(ordenInput, 'El orden es obligatorio');
                esValido = false;
            } else if (parseInt(ordenInput.value) < 1) {
                mostrarError(ordenInput, 'El orden debe ser un número positivo');
                esValido = false;
            }

            if (esValido) {
                this.submit();
            }
        });

        // Función para mostrar errores
        function mostrarError(input, mensaje) {
            const formGroup = input.closest('.form-group');
            input.classList.add('is-invalid');

            let feedback = formGroup.querySelector('.invalid-feedback');
            if (!feedback) {
                feedback = document.createElement('div');
                feedback.className = 'invalid-feedback';
                formGroup.appendChild(feedback);
            }
            feedback.textContent = mensaje;
        }

        // Función para quitar errores
        function quitarError(input) {
            input.classList.remove('is-invalid');
            const formGroup = input.closest('.form-group');
            const feedback = formGroup.querySelector('.invalid-feedback');
            if (feedback) {
                feedback.remove();
            }
        }
    } else {
        console.error('No se encontraron los elementos del formulario. Revisa los IDs en el HTML.');
    }
});
