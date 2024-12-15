from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    kakao_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True)  
    email = models.EmailField(unique=True, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('남', '남자'), ('여', '여자')], null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True) 
    last_login = models.DateTimeField(auto_now=True)

    # 토큰 필드 추가
    access_token = models.TextField(null=True, blank=True)  # Access 토큰
    refresh_token = models.TextField(null=True, blank=True)  # Refresh 토큰

    def __str__(self):
        return self.username


class Trip(models.Model):
    content = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
