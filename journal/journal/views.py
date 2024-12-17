from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from accounts.models import CustomUser, Question, Answer, TestResult
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.user.is_superuser:
        # Получаем всех пользователей, если текущий пользователь - суперпользователь
        users = CustomUser.objects.all()
        return render(request, '/home/businka/coursework/journal/accounts/templates/accounts/home.html', context = {'users': users, 'questions': None})  # Не показываем тест

    # Если не суперпользователь, показываем тест
    users = None
    questions = Question.objects.all()  # Получаем все вопросы для обычных пользователей

    return render(request, '/home/businka/coursework/journal/accounts/templates/accounts/home.html', context = {'users': users, 'questions': questions})



class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')