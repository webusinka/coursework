from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from accounts.models import CustomUser, Question, Answer, TestResult
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from collections import defaultdict

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

@login_required
def submit_test(request):
    if request.method == 'POST':
        user = request.user
        for question_id, answer_id in request.POST.items():
            if question_id.startswith('question_'):
                question = Question.objects.get(id=question_id.split('_')[1])
                selected_answer = Answer.objects.get(id=answer_id)
                # Сохраните результат в базе данных
                TestResult.objects.create(
                    user=user,
                    question=question,
                    selected_answer=selected_answer
                )
        messages.success(request, 'Ваши ответы успешно сохранены!')
        return redirect('results')  # Перенаправьте на страницу с результатами

    return redirect('home')  # Если не POST, перенаправьте на главную

def calculate_results(user):
    results = TestResult.objects.filter(user=user)
    
    # Словарь для хранения количества ответов по категориям
    category_counts = defaultdict(lambda: {'total': 0, 'correct': 0})

    for result in results:
        question = result.question
        category_counts[question.category]['total'] += 1
        if result.selected_answer.is_correct:
            category_counts[question.category]['correct'] += 1

    # Подсчет процентов
    percentages = {}
    for category, counts in category_counts.items():
        total = counts['total']
        correct = counts['correct']
        percentage = (correct / total * 100) if total > 0 else 0
        percentages[category] = {
            'correct': correct,
            'total': total,
            'percentage': percentage
        }

    return percentages

@login_required
def results(request):
    results = calculate_results(request.user)
    return render(request, '/home/businka/coursework/journal/accounts/templates/accounts/results.html', {'results': results})

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')