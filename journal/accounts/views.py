from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
import random
from .models import AcademicPerformance, id_Student_Group, Group

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('registrstion/login')

def register(request):
    groups = Group.objects.all()
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

            # Генерация случайных значений для AcademicPerformance
            attendance = random.uniform(0, 100)  # Случайное значение посещаемости от 0 до 100
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

            if user_type == 'student':  # Изменено на 'student'
                group_id = request.POST.get('group')  # Получаем ID группы из POST-запроса
                if group_id:
                    group = Group.objects.get(id=group_id)  # Получаем объект группы
                    id_Student_Group.objects.create(user=user, group=group)  # Сохраняем связь

            messages.success(request, 'Вы успешно зарегистрированы! Теперь вы можете войти.')
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'groups': groups})

