from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib import auth

# Create your views here.
def main_page(request):
    return render(request, 'main.html', {})
def login_page(request):
    login_data = LoginForm()
    return render(request, 'login_page.html', {'login_data':login_data})

def login_validate(request):
    login_data = LoginForm(request.POST)

    if login_data.is_valid():
        user = auth.authenticate(username=request.POST['id'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/')
        