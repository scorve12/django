from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    kakao_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True)  
    email = models.EmailField(unique=True, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('남', '남자'), ('여', '여자')], null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True) 
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
