from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import LoginForm


def home(request):
    return render(request, 'authentication/home.html')


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()

        if user:
            login(request, user)
            messages.info(request, 'Sesion iniciada correctamente')
            return redirect('authentication:home')

    context = {'form': form}
    return render(request, 'authentication/login.html', context)
