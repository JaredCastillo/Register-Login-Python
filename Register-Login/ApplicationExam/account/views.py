from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta


from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email = cd['email'], password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Credenciales corretas, bienvenido')
                else:
                    return HttpResponse('El usuario no existe')
            else:
                return HttpResponse('Contraseña o usuario no validos')
        else:
            form = LoginForm()
            return render(request, 'account/login.html',{'form': form})

@login_required
def dashboard(request):
    return render(request, 
                  'account/dashboard.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
           new_user = user_form.save(commit=False) 
           new_user.set_password(
               user_form.cleaned_data['password']
           )
           new_user.save()
           return render(request, 'account/register_done.html', {'new_user':new_user})
        else:
            return render(request, 'account/register.html', {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})
    
def recently_logged_in_users(request):
    recent_time = now() - timedelta(hours=1)
    recent_users = User.objects.filter(last_login__gte=recent_time)
    return render(request, 'account/recently_logged_users.html', {'recent_users': recent_users})
