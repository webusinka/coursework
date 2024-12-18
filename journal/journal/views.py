from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from accounts.models import CustomUser, Question, Answer, TestResult, AcademicPerformance
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

@login_required
def home(request):
    if request.user.is_staff:
        # Получаем всех пользователей, кроме суперпользователей
        users = CustomUser .objects.exclude(is_staff=True)
        # Получаем успеваемость для этих пользователей
        performances = AcademicPerformance.objects.filter(user__in=users)

        return render(request, 'accounts/home.html', context={'users': users, 'performances': performances, 'questions': None})  # Не показываем тест

    # Если студент, показываем тест
    users = None
    questions = Question.objects.all()

    return render(request, 'accounts/home.html', context={'users': users, 'questions': questions})

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
        return redirect('results')

    return redirect('home')

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
        sorted_percentages = dict(sorted(percentages.items(), key=lambda item: item[1]['percentage'], reverse=True))

    return sorted_percentages

@csrf_exempt
def update_performance(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        field = data.get('field')
        new_value = data.get('new_value')

        try:
            # Обновляем поля вручную
            update_fields = {}
            if field is not None:
                update_fields[field] = new_value

            # Обновляем объект AcademicPerformance по user_id
            AcademicPerformance.objects.filter(user_id=user_id).update(**update_fields)

            return JsonResponse({'status': 'success'})
        except AcademicPerformance.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Performance not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@login_required
def results(request):
    results = calculate_results(request.user)
    return render(request, 'accounts/results.html', {'results': results})

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')