# Используем официальный образ Python в качестве базового
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED 1

# Выполняем миграции
RUN python manage.py migrate

# Указываем команду для запуска приложения
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]