from django.contrib.auth.models import AbstractUser 
from django.db import models

class CustomUser (AbstractUser ):
    pass

class Profile(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Question(models.Model):
    text = models.CharField(max_length=255)

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