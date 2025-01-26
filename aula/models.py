from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

class Usuario(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('profesor', 'Profesor'),
        ('estudiante', 'Estudiante')
    ]
    rol = models.CharField(max_length=20, choices=ROLES)
    telefono = models.CharField(max_length=15, blank=True)

class Curso(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    profesor = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'profesor'})
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.titulo} {self.profesor}'

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    orden = models.IntegerField()

    def __str__(self):
        return f'{self.curso} {self.titulo}'

class Tarea(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('entregada', 'Entregada'),
        ('calificada', 'Calificada')
    ]
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f'{self.titulo} {self.modulo}'

class Entrega(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='entregas')
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    archivo = models.FileField(
        upload_to='entregas/',
        validators=[FileExtensionValidator(['pdf', 'docx', 'txt'])]
    )
    fecha_entrega = models.DateTimeField()

    def __str__(self):
        return f'{self.tarea} {self.estudiante} {str(self.archivo)}'

class Calificacion(models.Model):
    entrega = models.OneToOneField(Entrega, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    comentarios = models.TextField(blank=True)
    fecha_calificacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nota} {self.comentarios}'

class Foro(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} {self.curso}'

class Comentario(models.Model):
    foro = models.ForeignKey(Foro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario} {self.contenido}'

class Videoconferencia(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    enlace = models.URLField()
    fecha = models.DateTimeField()
    duracion = models.IntegerField(help_text="Duración en minutos")

    def __str__(self):
        return f'{self.titulo} {self.enlace} {str(self.fecha)}'