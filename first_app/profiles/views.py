from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def logout_view(request):
    logout(request)
    return redirect('/')

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user_name = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        print(user_name, password)
        user = authenticate(request, username=user_name, password=password)
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'profiles/form.html', {'form': form})

def register_view(request):
    form = RegisterForm(request.POST or None)
    print(form)

    if form.is_valid():
        user_name = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(user_name, email, password, is_staff=False)
        user.save()
        print(user_name, password, email)
        return redirect('/')
    return render(request, 'profiles/form.html', {'form': form, 'register' : True})


