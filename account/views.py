from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from account.forms import CreateUserForm, LoginForm
from a_users.models import Profile

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Welcome to my Social Media!')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
            return redirect('home')
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'account/register.html', context)


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Whats Up!')
                return redirect('home')
    context = {
        'login': form
    }
    return render(request, 'account/login.html', context=context)

def logout(request):
    auth.logout(request)
    messages.success(request, 'Why? 😢')
    return redirect('home')