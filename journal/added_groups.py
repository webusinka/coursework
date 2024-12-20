import os
import django
import random

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal.settings')
django.setup()

from accounts.models import Group, id_Student_Group
from django.contrib.auth import get_user_model

User  = get_user_model()

#accounts_group
#accounts_id_student_group

def populate():
    # Удаляем все существующие записи
    Group.objects.all().delete()
    groups_data = [
        'АБ-320',
        'АБ-321',
        'АБс-322',
        'АБс-323',
        'АБс-324',
        'АИ-32'
    ]

    # Создаем группы
    for group_name in groups_data:
        Group.objects.create(name=group_name)

    print("Таблица Group успешно заполнена.")

    id_Student_Group.objects.all().delete()

    # Получаем всех пользователей, исключая тех, у кого is_staff=True
    users = User.objects.filter(is_staff=False)

    # Проверяем, есть ли пользователи
    if not users.exists():
        print("Нет пользователей для заполнения таблицы id_Student_Group.")
        return

    # Назначаем пользователей в группы
    for user in users:
        # Случайно выбираем группу для пользователя
        group = random.choice(Group.objects.all())
        id_Student_Group.objects.get_or_create(user=user, group=group)

    print("Таблица id_Student_Group успешно заполнена.")

if __name__ == '__main__':
    populate()