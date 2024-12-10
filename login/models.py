from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    kakao_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)  # 닉네임
    email = models.EmailField(unique=True, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('남', '남자'), ('여', '여자')], null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)  # 나이
    last_login = models.DateTimeField(auto_now=True)  # 마지막 접속

    def __str__(self):
        return self.username
