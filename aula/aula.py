from django.utils import timezone

from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from .models import (
    Curso, Modulo, Tarea,
    Entrega, Calificacion,
    Foro, Comentario,
    Videoconferencia
)
from django.core.exceptions import PermissionDenied

from .forms import ModuloForm, TareaForm, CalificacionFormulario, EntregaFormulario
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404
from .models import Tarea, Entrega
from django.utils.timezone import now

#   Vistas de curso CRUD
class CursoListView(LoginRequiredMixin, ListView):
    model = Curso
    template_name = 'curso/curso_list.html'
    context_object_name = 'cursos'

    def get_queryset(self):
        return Curso.objects.all()

class CursoDetailView(LoginRequiredMixin, DetailView):
    model = Curso
    template_name = 'curso/curso_detail.html'

class CursoCreateView(LoginRequiredMixin, CreateView):
    model = Curso
    fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_fin']
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('curso_list')

    def form_valid(self, form):
        form.instance.profesor = self.request.user
        return super().form_valid(form)

class CursoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Curso
    fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_fin']
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('curso_list')

    def test_func(self):
        if self.request.user != self.get_object().profesor:
            messages.error(self.request, "No tienes permisos para editar este curso.")
            raise PermissionDenied("No tienes permisos para editar este curso.")
        return True

class CursoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Curso
    template_name = 'curso/curso_confirm_delete.html'
    success_url = reverse_lazy('curso_list')

    def test_func(self):
        if self.request.user != self.get_object().profesor:
            messages.error(self.request, "No tienes permisos para eliminar este curso.")
            raise PermissionDenied("No tienes permisos para eliminar este curso.")
        return True

#   Vistas de modulo CRUD
class ModuloListView(LoginRequiredMixin, ListView):
    model = Modulo
    template_name = 'modulo/modulo_list.html'
    context_object_name = 'modulos'

    def get_queryset(self):
        curso_id = self.kwargs.get('curso_id')  # Obtén curso_id de forma segura
        if curso_id:
            return Modulo.objects.filter(curso_id=curso_id)
        return Modulo.objects.all()  # Retorna todos los módulos si curso_id no está presente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso_id = self.kwargs.get('curso_id')  # Obtén curso_id de forma segura
        if curso_id:
            try:
                context['curso'] = Curso.objects.get(id=curso_id)
            except Curso.DoesNotExist:
                context['curso'] = None  # Maneja el caso donde el curso no existe
        else:
            context['curso'] = None  # Maneja el caso donde curso_id no está presente
        return context


class ModuloDetailView(LoginRequiredMixin, DetailView):
    model = Modulo
    template_name = 'modulo/modulo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tareas'] = self.object.tarea_set.all()
        return context

class ModuloCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Modulo
    form_class = ModuloForm
    template_name = 'modulo/modulo_form.html'

    def test_func(self):
        try:
            curso = get_object_or_404(Curso, id=self.kwargs['curso_id'])
        except Curso.DoesNotExist:
            messages.error(self.request, "Curso no encontrado.")
            raise PermissionDenied("Curso no encontrado.")
        if not curso.profesor or self.request.user != curso.profesor:
            messages.error(self.request, "No tienes permisos para crear módulos en este curso.")
            raise PermissionDenied("No tienes permisos para crear módulos en este curso.")
        return True

    def form_valid(self, form):
        form.instance.curso_id = self.kwargs['curso_id']
        return super().form_valid(form)

    def get_success_url(self):
        # Verifica que 'curso_id' esté presente al momento de obtener la URL
        return reverse_lazy('modulo_list', kwargs={'curso_id': self.kwargs['curso_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso_id = self.kwargs.get('curso_id')
        curso = get_object_or_404(Curso, pk=curso_id)
        context['curso'] = curso
        return context

class ModuloUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Modulo
    form_class = ModuloForm
    template_name = 'modulo/modulo_form.html'

    def test_func(self):
        if self.request.user != self.get_object().curso.profesor:
            messages.error(self.request, "No tienes permisos para editar este módulo.")
            raise PermissionDenied("No tienes permisos para editar este módulo.")
        return True

    def get_success_url(self):
        return reverse_lazy('modulo_detail', kwargs={'pk': self.object.pk})

class ModuloDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Modulo
    template_name = 'modulo/modulo_confirm_delete.html'

    def test_func(self):
        if self.request.user != self.get_object().curso.profesor:
            messages.error(self.request, "No tienes permisos para eliminar este módulo.")
            raise PermissionDenied("No tienes permisos para eliminar este módulo.")
        return True

    def get_success_url(self):
        return reverse_lazy('modulo_list', kwargs={'curso_id': self.object.curso_id})

#   Vistas de tarea CRUD
class TareaListView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = 'tarea/tarea_list.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        modulo_id = self.kwargs.get('modulo_id')
        modulo = get_object_or_404(Modulo, id=modulo_id)
        return Tarea.objects.filter(modulo=modulo)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        modulo_id = self.kwargs.get('modulo_id')
        context['modulo'] = get_object_or_404(Modulo, id=modulo_id)
        return context


class TareaEstudianteListView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = 'tarea/tarea_estudiante_list.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated or user.rol != 'estudiante':
            raise Http404('No tienes permisos para ver esta página')

        # Obtener los cursos en los que el estudiante está inscrito (relación implícita)
        cursos = Curso.objects.filter(modulo__tarea__entregas__estudiante=user)

        # Filtrar las tareas de los cursos en los que el estudiante está inscrito
        tareas = Tarea.objects.filter(modulo__curso__in=cursos)

        # Para cada tarea, verificar si el usuario ya la entregó
        for tarea in tareas:
            tarea.entregada = tarea.entregas.filter(estudiante=user).exists()

        # Filtrar las tareas de los módulos de los cursos en los que el estudiante está inscrito
        return tareas #Tarea.objects.filter(modulo__curso__in=cursos)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Obtener los cursos asociados al estudiante
        context['cursos'] = Curso.objects.filter(modulo__tarea__entregas__estudiante=user)
        context['titulo'] = 'Tareas del Estudiante'

        return context


class TareaDetailView(LoginRequiredMixin, DetailView):
    model = Tarea
    template_name = 'tarea/tarea_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario_actual = self.request.user
        context['entrega_existente'] = self.object.entregas.filter(estudiante=usuario_actual).first()
        return context

    def post(self, request, *args, **kwargs):
        tarea = self.get_object()
        usuario_actual = request.user
        archivo = request.FILES.get('archivo')

        if archivo:
            # Crear una nueva entrega
            Entrega.objects.create(
                tarea=tarea,
                estudiante=usuario_actual,
                archivo=archivo,
                fecha_entrega=now()
            )
            return redirect('tarea_detail',  pk=tarea.pk)

        return self.get(request, *args, **kwargs)

class TareaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tarea/tarea_form.html'

    def test_func(self):
        modulo = Modulo.objects.get(id=self.kwargs.get('modulo_id'))
        if self.request.user != modulo.curso.profesor:
            messages.error(self.request, "No tienes permisos para crear tareas en este módulo.")
            raise PermissionDenied("No tienes permisos para crear tareas en este módulo.")
        return True

    def form_valid(self, form):
        print("form_valid se está ejecutando")  # Verifica si la función se llama
        modulo_id = self.kwargs.get('modulo_id')
        print(f"modulo_id: {modulo_id}")  # Verifica el valor de modulo_id
        if not modulo_id:
            raise ValueError("modulo_id no está disponible")

        modulo = Modulo.objects.get(id=modulo_id)
        form.instance.modulo = modulo
        return super().form_valid(form)

    def get_success_url(self):
        modulo_id = self.kwargs.get('modulo_id')
        if not modulo_id:
            raise ValueError("modulo_id no está disponible en get_success_url")
        return reverse_lazy('tarea_list', kwargs={'modulo_id': modulo_id})


class TareaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tarea/tarea_form.html'

    def test_func(self):
        if self.request.user != self.get_object().modulo.curso.profesor:
            messages.error(self.request, "No tienes permisos para editar esta tarea.")
            raise PermissionDenied("No tienes permisos para editar esta tarea.")
        return True
    def get_queryset(self):
        return Tarea.objects.filter(modulo_id=self.kwargs['modulo_id'])

    def get_success_url(self):
        modulo_id = self.get_object().modulo.id
        return f"/modulo/{modulo_id}/tareas/"

class TareaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tarea
    template_name = 'tarea/tarea_confirm_delete.html'

    def test_func(self):
        if self.request.user != self.get_object().modulo.curso.profesor:
            messages.error(self.request, "No tienes permisos para eliminar esta tarea.")
            raise PermissionDenied("No tienes permisos para eliminar esta tarea.")
        return True

    def get_success_url(self):
        return reverse_lazy('tarea_list', kwargs={'modulo_id': self.object.modulo_id})

# Views de entregas
@login_required
def entregar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id)

    if request.user.rol != 'estudiante':
        # Redirigir si el usuario no es un estudiante
        return redirect('home')

    # Verificar si el estudiante ya ha entregado la tarea
    if Entrega.objects.filter(tarea=tarea, estudiante=request.user).exists():
        return render(request, 'error.html', {'mensaje': 'Ya has entregado esta tarea.'})

    if request.method == 'POST':
        form = EntregaFormulario(request.POST, request.FILES)
        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.tarea = tarea
            entrega.estudiante = request.user
            entrega.fecha_entrega = timezone.now()
            entrega.save()
            return redirect('tarea_list', modulo_id=tarea.modulo.id)  # Redirigir a una vista de tareas entregadas o listado

    else:
        form = EntregaFormulario()

    return render(request, 'tarea/entrega_form.html', {'form': form, 'tarea': tarea})


class EntregaListView(LoginRequiredMixin, ListView):
    model = Entrega
    template_name = 'entrega/listar_entregas.html'
    context_object_name = 'entregas'

    def get_queryset(self):
        from django.http import Http404
        user = self.request.user
        if not user.is_authenticated:
            raise Http404('No tienes permisos para ver esta página')

        # Si el usuario es un profesor, filtra las entregas de los cursos que enseña
        if user.rol == 'profesor':
            return Entrega.objects.filter(tarea__modulo__curso__profesor=user)

        # Si el usuario es un estudiante, filtra las entregas de ese estudiante
        elif user.rol == 'estudiante':
            return Entrega.objects.filter(estudiante=user)

        # Si el rol no es ni profesor ni estudiante, negar acceso
        raise Http404('No tienes permisos para ver esta página')


#   Views de calificacion
@login_required
def calificar_tarea(request, tarea_id, entrega_id=None):
    tarea = get_object_or_404(Tarea, pk=tarea_id)
    entrega = None
    if entrega_id:
        entrega = get_object_or_404(Entrega, pk=entrega_id)

    # Lógica para profesores y validaciones
    if request.user.rol != 'profesor' or tarea.modulo.curso.profesor != request.user:
        return redirect('home')

    # Resto de la lógica
    if request.method == 'POST':
        nota = request.POST.get('nota')
        comentarios = request.POST.get('comentarios')
        if entrega:
            Calificacion.objects.update_or_create(
                entrega=entrega,
                defaults={'nota': nota, 'comentarios': comentarios, 'fecha_calificacion': timezone.now()}
            )
        # Cambiar el estado de la tarea
        tarea.estado = 'calificada'
        tarea.save()

        return redirect('tarea_list', modulo_id=tarea.modulo.id)

    return render(request, 'tarea/calificar_tarea.html', {'tarea': tarea, 'entrega': entrega})


class CalificacionListView(LoginRequiredMixin, ListView):
    model = Calificacion
    template_name = 'calificaciones/listar_calificaciones.html'
    context_object_name = 'calificaciones'

    def get_queryset(self):
        from django.http import Http404
        """Filtra las calificaciones solo para las tareas del profesor actual"""
        user = self.request.user
        if not user.is_authenticated or (user.rol != 'profesor' and user.rol != 'estudiante'):
            raise Http404('No tienes permisos para ver esta página')

        if user.rol == 'profesor':
            # Si es profesor, muestra todas las calificaciones de sus cursos
            return Calificacion.objects.filter(entrega__tarea__modulo__curso__profesor=user)

        elif user.rol == 'estudiante':
            # Si es estudiante, solo muestra las calificaciones de sus propias entregas
            return Calificacion.objects.filter(entrega__estudiante=user)

        return Calificacion.objects.none()
