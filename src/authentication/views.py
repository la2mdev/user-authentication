from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import LoginForm, SignupForm, RegisterForm


def home(request):
    return render(request, 'authentication/home.html')


def login_view(request):
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
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'sesion cerrada correctamente')
        return redirect('authentication:home')


def signup_view(request):
    form = SignupForm(request.POST or None)

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
