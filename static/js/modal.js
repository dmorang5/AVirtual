const moduloModal = document.getElementById('moduloModal');
moduloModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget; // El botón que ha activado el modal
    const cursoId = button.getAttribute('data-curso-id'); // Obtener el curso_id del botón

    console.log("Curso ID:", cursoId); // Depuración

    if (cursoId) {
        const form = moduloModal.querySelector('form');
        const actionUrl = "{% url 'modulo_create' curso_id=0 %}".replace('0', cursoId);
        form.action = actionUrl;
    } else {
        console.error("Curso ID no encontrado.");
    }
});


