from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import CustomUser, Question, Answer, TestResult
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.user.is_superuser:
        # Получаем всех пользователей, если текущий пользователь - суперпользователь
        users = CustomUser .objects.all()
        return render(request, 'home.html', {'users': users, 'questions': None})  # Не показываем тест

    # Если не суперпользователь, показываем тест
    users = None
    questions = Question.objects.all()  # Получаем все вопросы для обычных пользователей

    return render(request, 'home.html', {'users': users, 'questions': questions})

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

