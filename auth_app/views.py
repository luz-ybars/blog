from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.conf import settings
from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                password = form.cleaned_data.get('password1')
                validate_password(password)
                user = form.save()
                invite_code = form.cleaned_data.get('invite_code')
                invite_target = getattr(settings, 'COLAB_INVITE_CODE', '')
                if invite_code and invite_target and invite_code == invite_target:
                    group, _ = Group.objects.get_or_create(name="Colaborador")
                else:
                    if invite_code and invite_code != invite_target:
                        messages.warning(request, 'Código de invitación inválido. Se te registró como Miembro.')
                    group, _ = Group.objects.get_or_create(name="Miembro")
                user.groups.add(group)
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.username}! Tu cuenta ha sido creada exitosamente.')
                return redirect('home')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
        else:
            if 'username' in form.errors:
                messages.error(request, 'El nombre de usuario ya existe o no es válido.')
            elif 'password1' in form.errors:
                messages.error(request, 'La contraseña no cumple con los requisitos de seguridad.')
            elif 'password2' in form.errors:
                messages.error(request, 'Las contraseñas no coinciden.')
            else:
                messages.error(request, 'Error en el registro. Verifica los datos ingresados.')
    else:
        form = RegistroForm()
    return render(request, 'auth/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido de vuelta, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Credenciales incorrectas. Verifica tu usuario y contraseña.')
        else:
            messages.error(request, 'Por favor, completa todos los campos correctamente.')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f'Has cerrado sesión correctamente. ¡Hasta pronto, {username}!')
    return redirect('home')