document.addEventListener("DOMContentLoaded", function () {
    const notaInput = document.getElementById("nota");
    const comentariosInput = document.getElementById("comentarios");
    const notaError = document.getElementById("notaError");
    const comentariosError = document.getElementById("comentariosError");

    const validarCalificacion = () => {
        let esValido = true;

        // Validar la nota
        const nota = parseFloat(notaInput.value);
        console.log('Nota ingresada:', nota); // Debugging
        if (isNaN(nota) || nota < 0 || nota > 10) {
            console.log('Error en la validación de la nota'); // Debugging
            notaError.textContent = "La nota debe ser un número entre 0 y 10.";
            notaError.style.display = "block";
            notaInput.classList.add("is-invalid");
            esValido = false;
        } else {
            notaError.style.display = "none";
            notaInput.classList.remove("is-invalid");
        }

        // Validar los comentarios
        if (comentariosInput.value.trim() === "") {
            comentariosError.textContent = "Los comentarios son obligatorios.";
            comentariosError.style.display = "block";
            comentariosInput.classList.add("is-invalid");
            esValido = false;
        } else {
            comentariosError.style.display = "none";
            comentariosInput.classList.remove("is-invalid");
        }

        return esValido;
    };

    // Agregar validación al enviar el formulario
    const form = document.querySelector("form");
    form.addEventListener("submit", function (event) {
        console.log("Validando formulario..."); // Debugging
        if (!validarCalificacion()) {
            console.log("Formulario no válido"); // Debugging
            event.preventDefault(); // Prevenir el envío del formulario si no es válido
        }
    });
});
