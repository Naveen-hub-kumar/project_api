

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import RegisterForm

# Register
def register_view(request):

    form = RegisterForm(request.POST or None)

    if form.is_valid():

        user = form.save()

        login(request, user)

        return redirect('dashboard')

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )

# Login
def login_view(request):

    form = AuthenticationForm(
        data=request.POST or None
    )

    if form.is_valid():

        user = form.get_user()

        login(request, user)

        return redirect('dashboard')

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )

# Logout
def logout_view(request):

    logout(request)

    return redirect('login')