from django.urls import path

from . import views
from .aula import (
    CursoListView, CursoDetailView, CursoCreateView, CursoUpdateView, CursoDeleteView,
    ModuloListView, ModuloDetailView, ModuloCreateView, ModuloUpdateView, ModuloDeleteView,
    TareaListView, TareaDetailView, TareaCreateView, TareaUpdateView, TareaDeleteView,
    entregar_tarea, calificar_tarea
)

urlpatterns = [
    # Rutas principales
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),

    # Rutas de curso
    path('curso/', CursoListView.as_view(), name='curso_list'),
    path('curso/<int:pk>/', CursoDetailView.as_view(), name='curso_detail'),
    path('curso/crear/', CursoCreateView.as_view(), name='curso_create'),
    path('curso/<int:pk>/editar/', CursoUpdateView.as_view(), name='curso_update'),
    path('curso/<int:pk>/eliminar/', CursoDeleteView.as_view(), name='curso_delete'),

    # Rutas de modulo
    path('modulos/<int:curso_id>/', ModuloListView.as_view(), name='modulo_list'),
    path('modulo/<int:pk>/', ModuloDetailView.as_view(), name='modulo_detail'),
    path('<int:curso_id>/modulo/crear/', ModuloCreateView.as_view(), name='modulo_create'),
    path('modulo/<int:pk>/editar/', ModuloUpdateView.as_view(), name='modulo_update'),
    path('modulo/<int:pk>/eliminar/', ModuloDeleteView.as_view(), name='modulo_delete'),

    # Rutas de tarea
    path('modulo/<int:modulo_id>/tarea/', TareaListView.as_view(), name='tarea_list'),
    path('tarea/<int:pk>/', TareaDetailView.as_view(), name='tarea_detail'),
    path('modulo/<int:modulo_id>/tarea/crear/', TareaCreateView.as_view(), name='tarea_create'),
    path('modulo/<int:modulo_id>/tarea/editar/<int:pk>/', TareaUpdateView.as_view(), name='tarea_update'),
    path('<int:pk>/eliminar/', TareaDeleteView.as_view(), name='tarea_delete'),
    path('entregar_tarea/<int:tarea_id>/', entregar_tarea, name='entregar_tarea'),
    path('tarea/<int:tarea_id>/calificar/', calificar_tarea, name='calificar_tarea_sin_entrega'),
    path('tarea/<int:tarea_id>/entrega/<int:entrega_id>/calificar/', calificar_tarea, name='calificar_tarea'),

]