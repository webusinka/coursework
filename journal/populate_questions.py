import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal.settings')
django.setup()

from accounts.models import Question, Answer

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

if __name__ == '__main__':
    populate()