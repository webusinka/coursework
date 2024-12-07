from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

def home(request):
    return render(request, 'accounts/home.html')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('registrstion/login')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрированы! Теперь вы можете войти.')
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

