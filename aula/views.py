from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request, 'home.html')

def register_view(request):
    from django.contrib.auth import login
    from .forms import CustomUserCreationForm
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('home')
        else:
            messages.error(request, 'El registro falló. Por favor corrija los errores')
    else:
        form = CustomUserCreationForm()
    return render(request, 'login/register.html', {'form': form})

def login_view(request):
    from django.contrib.auth import login, authenticate
    from .forms import LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Inicio de sesión exitosa!')
                return redirect('home')
            else:
                messages.error(request, 'Nombre de usuario o contraseña no validos.')
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, 'Te has desconectado.')
    return redirect('login')