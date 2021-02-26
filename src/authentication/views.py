from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import LoginForm, SignupForm, RegisterForm, ChangeProfileForm


def home(request):
    return render(request, 'authentication/home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('authentication:home')

    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()

        if user:
            login(request, user)
            messages.info(request, 'sesion iniciada correctamente')
            return redirect('authentication:home')

    context = {'form': form}
    return render(request, 'authentication/login.html', context)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('authentication:home')

    if request.method == 'POST':
        logout(request)
        messages.info(request, 'sesion cerrada correctamente')
        return redirect('authentication:home')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('authentication:home')

    form = SignupForm(request.POST or None)
    print(form.is_valid())

    if not form.is_valid():
        for error in form.non_field_errors():
            print(error)

    if request.method == 'POST' and form.is_valid():
        user = form.save()

        if user:
            login(request, user)
            messages.info(request, 'usuario creado exitosamente')
            return redirect('authentication:home')

    context = {'form': form}
    return render(request, 'authentication/signup.html', context)


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()

        if user:
            login(request, user)
            messages.info(request, 'usuario regustrado exitosamente')
            return redirect('authentication:home')

    context = {'form': form}
    return render(request, 'authentication/register.html', context)


def edit_view(request):
    form = ChangeProfileForm(request.POST or None, instance=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.info(request, 'datos actualizados exitosamente')
        return redirect('authentication:home')

    context = {'form': form}
    return render(request, 'authentication/edit_profile.html', context)


def change_password_view(request):
    form = PasswordChangeForm(data=request.POST or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.info(request, 'contraseña cambiada')
        return redirect('authentication:home')
    
    context = {'form': form}
    return render(request, 'authentication/change_password.html', context)
