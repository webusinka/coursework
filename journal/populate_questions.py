import os
import django
import random

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal.settings')
django.setup()

from accounts.models import Question, Answer, AcademicPerformance
from django.contrib.auth import get_user_model

User  = get_user_model()

def populate():
    # Удаляем все существующие записи
    Answer.objects.all().delete()  # Сначала удаляем ответы
    Question.objects.all().delete()  # Затем удаляем вопросы

    # Пример вопросов и ответов
    questions_data = [
        {
            'text': 'Разрабатывать законы в сфере ИБ',
            'category': 'Бумажная ИБ',
            'answers': [
                {'text': 'Больше да', 'is_correct': True},
                {'text': 'Больше нет', 'is_correct': False},
            ]
        },
        {
            'text': 'Внедрение новых методов защиты через шифрование',
            'category': 'Криптография',
            'answers': [
                {'text': 'Больше да', 'is_correct': True},
                {'text': 'Больше нет', 'is_correct': False},
            ]
        },
        {
            'text': 'Разрабатывать комплекс защиты периметра',
            'category': 'Архитектура ИБ',
            'answers': [
                {'text': 'Больше да', 'is_correct': True},
                {'text': 'Больше нет', 'is_correct': False},
            ]
        },
        {
            'text': 'Разбирать файлы вирусов и получать их код из (.exe) файлов',
            'category': 'Реверс-инжиниринг',
            'answers': [
                {'text': 'Больше да', 'is_correct': True},
                {'text': 'Больше нет', 'is_correct': False},
            ]
        },
        {
            'text': 'Моделировать атаку и анализировать утечку данных',
            'category': 'Пинтестирование',
            'answers': [
                {'text': 'Больше да', 'is_correct': True},
                {'text': 'Больше нет', 'is_correct': False},
            ]
        },
        {
            'text': 'Разработка защиты серверной инфраструктуры и их внедрение',
            'category': 'Архитектура ИБ',
            'answers': [
                {'text': 'Больше да', 'is_correct': True},
                {'text': 'Больше нет', 'is_correct': False},
            ]
        },
        {
            'text': 'Исследовать шпионское ПО и его возможности',
            'category': 'Реверс-инжиниринг',
            'answers': [
                {'text': 'Больше да', 'is_correct': True},
                {'text': 'Больше нет', 'is_correct': False},
            ]
        },
        {
            'text': 'Проникать в систему написанную другими',
            'category': 'Пинтестирование',
            'answers': [
                {'text': 'Больше да', 'is_correct': True},
                {'text': 'Больше нет', 'is_correct': False},
            ]
        },
        {
            'text': 'Исследовать старые шифры и создавать их аналоги или новые',
            'category': 'Криптография',
            'answers': [
                {'text': 'Больше да', 'is_correct': True},
                {'text': 'Больше нет', 'is_correct': False},
            ]
        },
        {
            'text': 'Оценивать важность защиты информации и составлять документацию',
            'category': 'Бумажная ИБ',
            'answers': [
                {'text': 'Больше да', 'is_correct': True},
                {'text': 'Больше нет', 'is_correct': False},
            ]
        },
    ]

    # Цикл для создания вопросов и ответов
    for question_data in questions_data:
        question = Question.objects.create(
            text=question_data['text'],
            category=question_data['category']  # Указываем категорию
        )
        for answer_data in question_data['answers']:
            Answer.objects.create(
                question=question,
                text=answer_data['text'],
                is_correct=answer_data['is_correct']
            )

    print("Вопросы и ответы успешно созданы.")

    # Удаляем все существующие записи
    AcademicPerformance.objects.all().delete()

    # Получаем всех пользователей, исключая тех, у кого is_staff=True
    users = User.objects.filter(is_staff=False)

    # Проверяем, есть ли пользователи
    if not users.exists():
        print("Нет пользователей для заполнения таблицы AcademicPerformance.")
        return

    # Пример данных для заполнения
    for user in users:
        attendance = random.uniform(50, 100)  # Случайное значение посещаемости от 0 до 100
        oib_score = random.choice([3, 4, 5])  # Случайная оценка OIB
        programming_score = random.choice([3, 4, 5])  # Случайная оценка по программированию
        os_security_score = random.choice([3, 4, 5])  # Случайная оценка по безопасности ОС
        direction_comment = "Комментарий для пользователя {}".format(user.username)  # Комментарий

        # Создаем запись в таблице AcademicPerformance
        AcademicPerformance.objects.create(
            user=user,
            attendance=attendance,
            oib_score=oib_score,
            programming_score=programming_score,
            os_security_score=os_security_score,
            direction_comment=direction_comment
        )

    print("Таблица AcademicPerformance успешно заполнена.")

if __name__ == '__main__':
    populate()