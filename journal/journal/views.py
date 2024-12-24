from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from accounts.models import CustomUser, Question, Answer, TestResult, AcademicPerformance, Group, id_Student_Group
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

@login_required
def home(request):
    groups = Group.objects.all()  # Получаем все группы

    if request.user.is_staff:
        # Получаем ID группы из GET-запроса, если он есть
        group_id = request.GET.get('group_id')

        if group_id:
            # Фильтруем пользователей по выбранной группе
            users = CustomUser .objects.filter(id_student_group__group_id=group_id)
        else:
            # Если группа не выбрана, получаем всех пользователей без группы, кроме суперпользователей
            users = CustomUser .objects.exclude(id__in=id_Student_Group.objects.values('user_id')).exclude(is_staff=True)

        # Получаем успеваемость для этих пользователей
        performances = AcademicPerformance.objects.filter(user__in=users)

        return render(request, 'accounts/home.html', context={
            'users': users,
            'performances': performances,
            'questions': None,
            'groups': groups  # Передаем группы в контекст
        })  # Не показываем тест

    # Если студент, показываем тест
    users = None
    questions = Question.objects.all()

    return render(request, 'accounts/home.html', context={'users': users, 'questions': questions})

def edit_testing(request):
    questions = Question.objects.all()
    unique_categories = Question.objects.values('category').distinct()
    if request.method == 'GET':
        return render(request, 'accounts/edit_testing.html', context={'questions': questions, 'unique_categories':unique_categories})

@login_required
def assign_group(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        new_group_id = request.POST.get('new_group')

        if student_id and new_group_id:
            # Получаем или создаем запись в id_Student_Group
            student_group, created = id_Student_Group.objects.get_or_create(user_id=student_id)

            # Обновляем группу
            student_group.group_id = new_group_id
            student_group.save()

            return redirect('home')  # Перенаправляем на главную страницу после назначения группы
        else:
            return HttpResponse("Ошибка: Не указаны студент или группа.", status=400)

    return HttpResponse("Метод не разрешен.", status=405)

def add_group(request):
    groups = Group.objects.all()
    error_message = None  # Переменная для хранения сообщения об ошибке

    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        if group_name:
            # Проверяем, существует ли группа с таким названием
            if Group.objects.filter(name=group_name).exists():
                error_message = "Такая группа уже существует."  # Устанавливаем сообщение об ошибке
            else:
                # Создаем новую группу
                Group.objects.create(name=group_name)
                return redirect('add_group')  # Перенаправляем на ту же страницу после добавления

    return render(request, 'accounts/add_group.html', context={'groups': groups, 'error_message': error_message})

@require_http_methods(["DELETE"])
def delete_group(request, group_id):
    try:
        # Получаем группу и связанных с ней пользователей
        group = Group.objects.get(id=group_id)
        users_in_group = id_Student_Group.objects.filter(group=group).select_related('user')

        # Удаляем все записи из id_Student_Group, связанные с группой
        users_in_group.delete()
        
        # Теперь удаляем саму группу
        group.delete()
        
        # Возвращаем список пользователей, которые были в удаленной группе
        return JsonResponse({
            'message': 'Группа успешно удалена.',
            'users': [{'id': user.user.id, 'username': user.user.username} for user in users_in_group]
        }, status=204)
    except Group.DoesNotExist:
        return JsonResponse({'error': 'Группа не найдена.'}, status=404)
    
    
def get_question_category(request, question_id):
    try:
        question = Question.objects.get(id=question_id)  # Получаем вопрос по ID
        category = question.category  # Получаем категорию
        return JsonResponse({'category': category})  # Возвращаем категорию в формате JSON
    except Question.DoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)

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

@login_required
def results(request):
    results = calculate_results(request.user)
    return render(request, 'accounts/results.html', {'results': results})

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

@csrf_exempt
def save_testing_changes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        new_category = data.get('new_category')

        if action == 'add':
            question_text = data.get('question')
            category = data.get('category')
            if new_category != "":
                category = new_category

            if question_text and category:
                # Создаем новый вопрос и добавляем ответы
                new_question = Question.objects.create(text=question_text, category=category)
                Answer.objects.create(question_id=new_question.id, text='Больше да', is_correct=True)
                Answer.objects.create(question_id=new_question.id, text='Больше нет', is_correct=False)

                return JsonResponse({'status': 'success', 'message': 'Вопрос успешно добавлен!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Необходимо заполнить все поля.'}, status=400)

        elif action == 'delete':
            question_id = data.get('delete_question_id')
            if question_id:
                try:
                    # Находим вопрос по ID и удаляем его вместе с ответами
                    question = Question.objects.get(id=question_id)
                    question.delete()  # Это также удалит все связанные ответы из-за on_delete=models.CASCADE

                    return JsonResponse({'status': 'success', 'message': 'Вопрос успешно удален!'})
                except Question.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Вопрос не найден.'}, status=404)
            else:
                return JsonResponse({'status': 'error', 'message': 'Необходимо указать ID вопроса для удаления.'}, status=400)

        elif action == 'update':
            question_id = data.get('question_id')
            new_question_text = data.get('question')
            new_category = data.get('category')
            if new_category == "":
                # Если новая категория введена, используем её
                new_category = data.get('new_category')
            
            if question_id and new_question_text and new_category:
                try:
                    # Находим вопрос по ID и обновляем его текст и категорию
                    question = Question.objects.get(id=question_id)
                    question.text = new_question_text
                    question.category = new_category
                    question.save()  # Сохраняем изменения

                    return JsonResponse({'status': 'success', 'message': 'Вопрос успешно обновлен!'})
                except Question.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Вопрос не найден.'}, status=404)
            else:
                return JsonResponse({'status': 'error', 'message': 'Необходимо указать ID вопроса, текст и категорию для обновления.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Ошибка при сохранении изменений.'}, status=400)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')