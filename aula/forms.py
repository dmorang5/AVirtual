from django import forms
from django.contrib.auth.forms import UserCreationForm
from aula.models import Usuario
from .models import Curso, Modulo, Tarea, Entrega, Calificacion
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

#   Forms de Login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

#   Forms de USUARIO
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol']
        widgets = {
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }


#   Forms de curso
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del curso'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            if fecha_inicio > fecha_fin:
                raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin")
            if fecha_inicio < timezone.now().date():
                raise ValidationError("La fecha de inicio no puede ser en el pasado")
            if fecha_fin < timezone.now().date():
                raise ValidationError("La fecha de fin no puede ser en el pasado")

        # Validar longitud del título
        titulo = cleaned_data.get('titulo')
        if titulo and (len(titulo) < 5 or len(titulo) > 100):
            raise ValidationError("El título debe tener entre 5 y 100 caracteres")

        return cleaned_data

    def clean_titulo(self):
        # Validación adicional específica para el título
        titulo = self.cleaned_data['titulo']
        # Evitar títulos con solo espacios
        if not titulo.strip():
            raise ValidationError("El título no puede estar vacío")
        return titulo

#   Forms de Modulo
class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ['titulo', 'descripcion', 'orden']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del módulo'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del módulo'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            })
        }

    def clean_titulo(self):
        titulo = self.cleaned_data['titulo']
        if len(titulo) < 3:
            raise ValidationError("El título debe tener al menos 3 caracteres")
        return titulo

    def clean_orden(self):
        orden = self.cleaned_data['orden']
        if orden < 1:
            raise ValidationError("El orden debe ser un número positivo")
        return orden

    def clean(self):
        cleaned_data = super().clean()
        titulo = cleaned_data.get('titulo')
        descripcion = cleaned_data.get('descripcion')

        if titulo and descripcion and titulo.lower() in descripcion.lower():
            raise ValidationError("El título no debe estar repetido en la descripción")

        return cleaned_data

#   Forms de Tarea
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_limite', 'estado']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_limite': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'form-select'})
        }

    def clean_titulo(self):
        titulo = self.cleaned_data['titulo']
        if len(titulo) < 5:
            raise ValidationError("El título debe tener al menos 5 caracteres")
        return titulo

    def clean_fecha_limite(self):
        fecha_limite = self.cleaned_data['fecha_limite']
        if fecha_limite <= timezone.now():
            raise ValidationError("La fecha límite debe ser futura")
        return fecha_limite

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

#   Forms de entrega
class EntregaFormulario(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['archivo']

    def __init__(self, *args, **kwargs):
        super(EntregaFormulario, self).__init__(*args, **kwargs)
        self.fields['archivo'].widget.attrs.update({'accept': '.pdf,.docx,.txt'})

#   Forms de calificacion
class CalificacionFormulario(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['nota', 'comentarios']
        widgets = {
            'nota': forms.NumberInput(attrs={'min': 0, 'max': 10}),
            'comentarios': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

        # Validación personalizada para el campo 'nota'
    def clean_nota(self):
        nota = self.cleaned_data.get('nota')

        if nota < 0 or nota > 10:
            raise ValidationError('La nota debe estar entre 0 y 10.')

        return nota
