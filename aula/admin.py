from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Curso, Modulo,
    Tarea, Entrega, Calificacion,
    Foro, Comentario, Videoconferencia
)

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'is_staff')
    list_filter = ('rol', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rol', 'foto_perfil')}),
    )

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'profesor', 'fecha_inicio', 'fecha_fin', 'activo')
    list_filter = ('profesor', 'activo', 'fecha_inicio')
    search_fields = ('titulo', 'descripcion')

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'orden')
    list_filter = ('curso',)
    search_fields = ('titulo',)

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'modulo', 'fecha_creacion', 'fecha_limite', 'estado')
    list_filter = ('estado', 'fecha_limite')
    search_fields = ('titulo', 'descripcion')

@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ('tarea', 'estudiante', 'fecha_entrega')
    list_filter = ('fecha_entrega', 'tarea')
    search_fields = ('estudiante__username',)

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('entrega', 'nota', 'fecha_calificacion')
    list_filter = ('nota', 'fecha_calificacion')

@admin.register(Foro)
class ForoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'fecha_creacion')
    list_filter = ('curso',)
    search_fields = ('titulo', 'descripcion')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'foro', 'fecha_creacion')
    list_filter = ('foro', 'fecha_creacion')

@admin.register(Videoconferencia)
class VideoconferenciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'fecha', 'duracion')
    list_filter = ('curso', 'fecha')
    search_fields = ('titulo',)