from django.contrib.auth.models import AbstractUser 
from django.db import models

class CustomUser (AbstractUser ):
    pass

class Profile(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username