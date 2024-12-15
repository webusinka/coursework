# populate_questions.py
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal.settings')
django.setup()

from accounts.models import Question, Answer

def populate():
    # Пример вопросов и ответов
    questions_data = [
        {
            'text': 'Какой ваш любимый цвет?',
            'answers': [
                {'text': 'Красный', 'is_correct': True},
                {'text': 'Синий', 'is_correct': False},
                {'text': 'Зеленый', 'is_correct': False},
            ]
        },
        {
            'text': 'Какой ваш любимый язык программирования?',
            'answers': [
                {'text': 'Python', 'is_correct': True},
                {'text': 'Java', 'is_correct': False},
                {'text': 'C++', 'is_correct': False},
            ]
        },
    ]

    for question_data in questions_data:
        question = Question.objects.create(text=question_data['text'])
        for answer_data in question_data['answers']:
            Answer.objects.create(
                question=question,
                text=answer_data['text'],
                is_correct=answer_data['is_correct']
            )

if __name__ == '__main__':
    populate()