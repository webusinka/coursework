from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('registrstion/login')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Не сохраняем пользователя сразу
            user_type = request.POST.get('user_type')  # Получаем тип пользователя

            if user_type == 'staff':
                user.is_staff = True  # Устанавливаем флаг is_staff в True
            else:
                user.is_staff = False  # Устанавливаем флаг is_staff в False (по умолчанию)

            user.save()  # Сохраняем пользователя
            messages.success(request, 'Вы успешно зарегистрированы! Теперь вы можете войти.')
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

