from django.contrib.auth.models import AbstractUser 
from django.db import models
import random

class CustomUser (AbstractUser ):
    pass

class Profile(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Question(models.Model):
    text = models.CharField(max_length=255)
    category = models.CharField(max_length=100)  # Добавлено поле для категории

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class TestResult(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.question.text} - {self.selected_answer.text}"

class AcademicPerformance(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)  # Измените на CustomUser 
    attendance = models.FloatField(default=random.uniform(0, 100))  # Посещаемость от 0 до 100%
    oib_score = models.IntegerField(choices=[(i, str(i)) for i in range(2, 6)], default=2)  # Оценка по ОИБ
    programming_score = models.IntegerField(choices=[(i, str(i)) for i in range(2, 6)], default=2)  # Оценка по программированию
    os_security_score = models.IntegerField(choices=[(i, str(i)) for i in range(2, 6)], default=2)  # Оценка по безопасности ОС
    direction_comment = models.CharField(max_length=255, blank=True)  # Комментарий по направлению

    def save(self, *args, **kwargs):
        # Вычисляем комментарий по направлению перед сохранением
        self.direction_comment = self.calculate_direction_comment()
        super().save(*args, **kwargs)

    def calculate_direction_comment(self):
        # Вычисляем средний балл
        average_score = (self.oib_score + self.programming_score + self.os_security_score) / 3
        # Проверяем условия для комментария
        if average_score < 3 or self.attendance < 50:
            return "Рекомендуется перевестись"
        else:
            # Определяем предмет с наивысшим баллом
            highest_score_subject = max(self.oib_score, self.programming_score, self.os_security_score)
            if highest_score_subject == self.oib_score:
                return "Наивысший балл по ОИБ"
            elif highest_score_subject == self.programming_score:
                return "Наивысший балл по программированию"
            else:
                return "Наивысший балл по безопасности ОС"

    def __str__(self):
        return f"{self.user.username} - Успеваемость"